# pdf_utils.py - Updated with agent tracking

import PyPDF2
import re
import time
from tracker_integration import get_tracker, get_calc


def clean_extracted_text(text: str) -> str:
    """
    Smart cleaning for PDFs with character spacing.
    """
    
    # Step 1: Fix character spacing aggressively
    for _ in range(15):
        text = re.sub(r'([A-Za-z0-9]) ([A-Za-z0-9])', r'\1\2', text)
    
    # Step 2: Add spaces back where needed
    text = re.sub(r'\.([A-Z])', r'. \1', text)
    text = re.sub(r',([A-Za-z])', r', \1', text)
    text = re.sub(r'([A-Za-z])\(', r'\1 (', text)
    text = re.sub(r'\)([A-Za-z])', r') \1', text)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    
    # Clean up excessive whitespace
    text = re.sub(r' {2,}', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


def extract_text_from_pdf(pdf_file, track: bool = True) -> str:
    """
    Extract text from PDF with aggressive cleaning and agent tracking.
    
    Args:
        pdf_file: File path or file-like object
        track: Whether to log actions and rewards (default: True)
    
    Returns:
        Cleaned text content
    """
    tracker = get_tracker()
    calc = get_calc()
    
    # Get filename for logging
    if hasattr(pdf_file, 'name'):
        filename = pdf_file.name
    elif isinstance(pdf_file, str):
        filename = pdf_file.split('/')[-1]
    else:
        filename = "unknown.pdf"
    
    # LOG ACTION: Start extraction
    start_time = time.time()
    if track:
        tracker.log_action("extract_pdf", 
                          filename=filename,
                          file_type="pdf")
    
    try:
        # Handle both file path and file-like object
        if isinstance(pdf_file, str):
            pdf_reader = PyPDF2.PdfReader(pdf_file)
        else:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        num_pages = len(pdf_reader.pages)
        
        if track:
            tracker.log_action("read_pdf_pages", 
                              num_pages=num_pages,
                              filename=filename)
        
        text = ""
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        extraction_duration = time.time() - start_time
        
        print(f" Raw extraction: {len(text)} chars from {num_pages} pages")
        
        if not text.strip():
            if track:
                tracker.add_reward(calc.error_penalty(), 
                                 "Empty PDF or encrypted")
            raise ValueError("No text could be extracted from PDF")
        
        # REWARD: Successful extraction
        if track:
            tracker.add_reward(calc.task_completion(True), 
                             f"Extracted {len(text)} chars from {num_pages} pages")
            tracker.add_reward(calc.response_time(extraction_duration, 5.0),
                             f"Extraction time: {extraction_duration:.2f}s")
        
        # Apply aggressive cleaning
        clean_start = time.time()
        if track:
            tracker.log_action("clean_text", 
                              original_length=len(text))
        
        cleaned_text = clean_extracted_text(text)
        clean_duration = time.time() - clean_start
        
        print(f" After cleaning: {len(cleaned_text)} chars")
        
        # Sanity check - make sure we didn't destroy the text
        if len(cleaned_text) < len(text) * 0.2:
            print(" Cleaning removed too much text, using raw version")
            if track:
                tracker.add_reward(-2, "Cleaning too aggressive, reverted")
            cleaned_text = text
        else:
            if track:
                tracker.add_reward(calc.task_completion(True), 
                                 "Text cleaned successfully")
                tracker.add_reward(calc.response_time(clean_duration, 1.0),
                                 f"Clean time: {clean_duration:.2f}s")
        
        # Quality rewards based on content
        if track:
            if len(cleaned_text) > 5000:
                tracker.add_reward(5, "Large document (>5000 chars)")
            elif len(cleaned_text) > 1000:
                tracker.add_reward(3, "Medium document (>1000 chars)")
            else:
                tracker.add_reward(1, "Small document")
            
            # Bonus for multi-page documents
            if num_pages > 10:
                tracker.add_reward(3, f"Multi-page document ({num_pages} pages)")
        
        total_duration = time.time() - start_time
        print(f"⏱️ Total PDF processing: {total_duration:.2f}s")
        
        return cleaned_text
        
    except Exception as e:
        print(f" Error extracting PDF: {e}")
        if track:
            tracker.add_reward(calc.error_penalty(), 
                             f"PDF extraction failed: {str(e)}")
        raise


def extract_text_with_pdfplumber(pdf_file, track: bool = True):
    """
    Alternative extraction using pdfplumber with tracking.
    """
    tracker = get_tracker()
    calc = get_calc()
    
    if track:
        tracker.log_action("extract_with_pdfplumber",
                          method="pdfplumber")
    
    try:
        import pdfplumber
        
        start = time.time()
        
        if isinstance(pdf_file, str):
            pdf = pdfplumber.open(pdf_file)
        else:
            pdf = pdfplumber.open(pdf_file)
        
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        pdf.close()
        
        duration = time.time() - start
        
        print(f" PDFPlumber extracted: {len(text)} chars")
        
        if track:
            tracker.add_reward(calc.task_completion(True), 
                             "PDFPlumber extraction successful")
            tracker.add_reward(calc.response_time(duration, 5.0),
                             f"Time: {duration:.2f}s")
        
        return clean_extracted_text(text)
        
    except ImportError:
        print(" pdfplumber not installed. Using PyPDF2 instead.")
        if track:
            tracker.add_reward(-1, "PDFPlumber not available")
        return extract_text_from_pdf(pdf_file, track=track)
    except Exception as e:
        print(f"❌ PDFPlumber error: {e}")
        if track:
            tracker.add_reward(calc.error_penalty(), 
                             f"PDFPlumber error: {str(e)}")
        raise


if __name__ == "__main__":
    import sys
    
    # Test the cleaning function
    test_cases = [
        ("M a y  2 0 2 5  -  A u g  2 0 2 5", "May 2025 - Aug 2025"),
        ("G e e k s f o r G e e k s", "GeeksforGeeks"),
        ("P y t h o n  p r o g r a m m i n g", "Python programming"),
        ("5 4 0  p r o b l e m s", "540 problems"),
        ("Normal text should stay", "Normal text should stay"),
    ]
    
    print(" Testing Text Cleaning\n" + "="*60)
    all_passed = True
    for test_input, expected in test_cases:
        cleaned = clean_extracted_text(test_input)
        passed = cleaned == expected
        status = "✅" if passed else "❌"
        
        print(f"{status} Input:    {test_input}")
        print(f"   Expected: {expected}")
        print(f"   Got:      {cleaned}")
        print("-" * 60)
        
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n All cleaning tests passed!")
    else:
        print("\n Some tests failed - review above")
    
    # Test on actual PDF if provided
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        print(f"\n Testing on: {pdf_path}")
        text = extract_text_from_pdf(pdf_path)
        print(f"\n Extracted {len(text)} characters")
        print(f"\n First 500 characters:\n{text[:500]}")
        
        # Show tracker state
        tracker = get_tracker()
        tracker.display_state()