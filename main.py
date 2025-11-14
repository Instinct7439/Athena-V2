# main.py - Updated with research paper fetching capability

import requests
from paper_fetcher import PaperFetcher, ResearchPaper
from typing import List

OLLAMA_API_URL = "http://localhost:11434/api/generate"


def research_topic(topic: str, skip_tools: bool = False, fetch_papers: bool = True, 
                   max_papers: int = 5) -> str:
    """
    Research a topic by:
    1. Fetching relevant research papers from arXiv and Semantic Scholar
    2. Synthesizing the information using local LLM
    
    Args:
        topic: Research topic or query
        skip_tools: If True, skip paper fetching and just use LLM
        fetch_papers: Whether to fetch actual research papers
        max_papers: Maximum number of papers to fetch
    
    Returns:
        Comprehensive research summary
    """
    
    # Skip paper fetching for chunk summarization
    if skip_tools or not fetch_papers:
        return _generate_summary_only(topic)
    
    print(f"\n{'='*70}")
    print(f"🔬 RESEARCHING TOPIC: {topic}")
    print(f"{'='*70}\n")
    
    # Step 1: Fetch research papers
    print("📚 Step 1: Fetching research papers...")
    fetcher = PaperFetcher()
    
    try:
        papers = fetcher.search_papers(
            query=topic,
            max_results=max_papers,
            sources=['arxiv', 'semantic_scholar']
        )
        
        if not papers:
            print("⚠️ No papers found, generating summary from LLM knowledge...")
            return _generate_summary_only(topic)
        
        print(f"✅ Retrieved {len(papers)} papers\n")
        
    except Exception as e:
        print(f"❌ Error fetching papers: {e}")
        print("⚠️ Falling back to LLM-only summary...")
        return _generate_summary_only(topic)
    
    # Step 2: Build context from papers
    print("📝 Step 2: Processing paper abstracts...")
    context = _build_research_context(papers)
    
    # Step 3: Generate comprehensive summary
    print("🧠 Step 3: Generating comprehensive analysis...\n")
    summary = _generate_research_summary(topic, papers, context)
    
    return summary


def _build_research_context(papers: List[ResearchPaper]) -> str:
    """Build research context from papers"""
    
    context_parts = []
    
    for i, paper in enumerate(papers, 1):
        authors = ", ".join(paper.authors[:3])
        if len(paper.authors) > 3:
            authors += " et al."
        
        context_parts.append(f"""
[Paper {i}] {paper.title}
Authors: {authors}
Year: {paper.year}
Source: {paper.source}
Citations: {paper.citations if paper.citations > 0 else 'N/A'}
Abstract: {paper.abstract}
""".strip())
    
    return "\n\n---\n\n".join(context_parts)


def _generate_research_summary(topic: str, papers: List[ResearchPaper], 
                               context: str) -> str:
    """Generate comprehensive research summary using LLM"""
    
    # Build paper list for reference
    paper_list = "\n".join([
        f"{i}. {paper.title} ({paper.year}) - {paper.authors[0]} et al."
        for i, paper in enumerate(papers, 1)
    ])
    
    prompt = f"""You are Athena, an expert AI research assistant. Analyze these recent research papers on "{topic}" and provide a comprehensive summary.

RESEARCH PAPERS:
{context}

Your task:
1. **Overview**: Provide a clear introduction to "{topic}" based on these papers
2. **Key Findings**: Summarize the main contributions and findings from each paper
3. **Common Themes**: Identify patterns, shared methodologies, or consensus across papers
4. **Recent Advances**: Highlight what's new or cutting-edge in this area
5. **Challenges & Future Work**: Discuss open problems and research directions mentioned
6. **Practical Impact**: Explain real-world applications and implications

Be specific and reference the papers by number [Paper 1], [Paper 2], etc.
Write in an academic yet accessible style. Aim for 800-1000 words.

PAPER REFERENCES:
{paper_list}

COMPREHENSIVE RESEARCH SUMMARY:"""

    try:
        payload = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.4,
                "num_predict": 1500,
                "num_ctx": 8192  # Larger context for multiple papers
            }
        }
        
        print("   🤖 Calling Ollama API...")
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=180)
        
        if response.status_code != 200:
            print(f"   ❌ API Error: {response.status_code}")
            return _fallback_summary(papers)
        
        data = response.json()
        summary = data.get("response", "").strip()
        
        if not summary:
            print("   ⚠️ Empty response from LLM")
            return _fallback_summary(papers)
        
        # Add paper references at the end
        full_summary = f"{summary}\n\n{'='*70}\n\n## 📚 SOURCE PAPERS\n\n"
        
        for i, paper in enumerate(papers, 1):
            authors = ", ".join(paper.authors[:3])
            if len(paper.authors) > 3:
                authors += f" et al. ({len(paper.authors)} authors)"
            
            full_summary += f"\n**[Paper {i}]** {paper.title}\n"
            full_summary += f"- **Authors:** {authors}\n"
            full_summary += f"- **Year:** {paper.year} | **Source:** {paper.source}"
            
            if paper.citations > 0:
                full_summary += f" | **Citations:** {paper.citations}"
            
            full_summary += f"\n- **Link:** {paper.url}\n"
            
            if paper.pdf_url:
                full_summary += f"- **PDF:** {paper.pdf_url}\n"
        
        print("   ✅ Summary generated\n")
        return full_summary
        
    except requests.exceptions.Timeout:
        print("   ⏱️ Request timed out")
        return _fallback_summary(papers)
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return _fallback_summary(papers)


def _generate_summary_only(topic: str) -> str:
    """Generate summary using only LLM knowledge (no paper fetching)"""
    
    prompt = f"""You are Athena, an expert AI research assistant. Provide a comprehensive overview of: "{topic}"

Include:
1. **Definition & Core Concepts**: What is this topic about?
2. **Key Methods & Techniques**: Main approaches used in this area
3. **Important Milestones**: Historical development and breakthroughs
4. **Current State**: What's the current state of research/practice?
5. **Applications**: Real-world use cases and impact
6. **Challenges**: Open problems and limitations
7. **Future Directions**: Where is this field heading?

Be specific, technical yet accessible. Aim for 600-800 words."""

    try:
        payload = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.4,
                "num_predict": 1200
            }
        }
        
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "Error generating summary").strip()
        else:
            return f"Error: API returned status {response.status_code}"
            
    except Exception as e:
        return f"Error generating summary: {str(e)}"


def _fallback_summary(papers: List[ResearchPaper]) -> str:
    """Fallback summary when LLM fails"""
    
    summary = "# Research Paper Summary\n\n"
    summary += f"Retrieved {len(papers)} relevant research papers:\n\n"
    summary += "---\n\n"
    
    for i, paper in enumerate(papers, 1):
        authors = ", ".join(paper.authors[:3])
        if len(paper.authors) > 3:
            authors += " et al."
        
        summary += f"## {i}. {paper.title}\n\n"
        summary += f"**Authors:** {authors}\n"
        summary += f"**Year:** {paper.year} | **Source:** {paper.source}"
        
        if paper.citations > 0:
            summary += f" | **Citations:** {paper.citations}"
        
        summary += f"\n\n**Abstract:**\n{paper.abstract}\n\n"
        summary += f"**Links:** [View Paper]({paper.url})"
        
        if paper.pdf_url:
            summary += f" | [PDF]({paper.pdf_url})"
        
        summary += "\n\n---\n\n"
    
    return summary


# =====================================================================
# 🧪 TEST
# =====================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("🧪 TESTING ENHANCED RESEARCH FUNCTION")
    print("=" * 70)
    
    test_topic = "transformer attention mechanisms in NLP"
    
    print(f"\n🔬 Testing with: '{test_topic}'\n")
    
    result = research_topic(
        topic=test_topic,
        fetch_papers=True,
        max_papers=5
    )
    
    print("\n" + "=" * 70)
    print("📊 RESULTS")
    print("=" * 70)
    print(result[:1000] + "...\n")
    
    print("✅ TEST COMPLETE!")
    print("\n💡 The function now:")
    print("   1. Fetches real papers from arXiv and Semantic Scholar")
    print("   2. Synthesizes information using local LLM")
    print("   3. Provides paper citations and links")
    print("   4. Falls back gracefully if paper fetching fails")