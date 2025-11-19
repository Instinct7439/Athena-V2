"""
Script to remove white background from Athena logo and resize it
Run this once to process your logo image
"""

from PIL import Image
import numpy as np

def remove_white_background(input_path, output_path, threshold=240, target_size=None):
    """
    Remove white background from an image and make it transparent
    
    Args:
        input_path: Path to input image (with white background)
        output_path: Path to save output image (with transparency)
        threshold: RGB value threshold for considering a pixel as "white" (default 240)
        target_size: Tuple (width, height) to resize, or None to keep original
    """
    print(f"📂 Opening: {input_path}")
    
    # Open the image
    img = Image.open(input_path)
    print(f"   Original size: {img.size}")
    
    # Convert to RGBA if not already
    img = img.convert("RGBA")
    
    # Get pixel data
    data = np.array(img)
    
    # Create mask for white/light pixels
    # A pixel is considered white if all RGB values are above threshold
    white_mask = (data[:, :, 0] > threshold) & \
                 (data[:, :, 1] > threshold) & \
                 (data[:, :, 2] > threshold)
    
    # Set alpha channel to 0 for white pixels (make transparent)
    data[:, :, 3] = np.where(white_mask, 0, data[:, :, 3])
    
    # Create new image
    result = Image.fromarray(data)
    
    # Resize if target size specified
    if target_size:
        result = result.resize(target_size, Image.Resampling.LANCZOS)
        print(f"   Resized to: {target_size}")
    
    # Save with transparency
    result.save(output_path, "PNG", optimize=True)
    print(f"✅ Saved transparent logo to: {output_path}")
    print(f"   Removed white pixels above RGB threshold: {threshold}")
    
    return result

if __name__ == "__main__":
    import os
    
    # Create assets directory if it doesn't exist
    if not os.path.exists("assets"):
        os.makedirs("assets")
        print("📁 Created 'assets' directory\n")
    
    # Define paths
    input_image = "assets/athena_owl.png"  # Your downloaded logo with white background
    output_image = "assets/athena_logo.png"  # Output with transparency
    
    # Target sizes for different uses
    # (width, height) - maintains aspect ratio
    target_size = (400, 400)  # Good size for sidebar
    
    try:
        # Process the logo
        result = remove_white_background(
            input_image, 
            output_image, 
            threshold=230,  # Slightly lower to catch off-white pixels
            target_size=target_size
        )
        
        print("\n✨ Success! Your logo is now ready to use in the app.")
        print("   ✓ White background removed")
        print("   ✓ Made transparent")
        print("   ✓ Optimized size")
        print("\n💡 The logo will now blend perfectly with your dark theme!")
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{input_image}'\n")
        print("Please:")
        print("1. Right-click the owl logo image and 'Save As' → 'athena_owl.png'")
        print("2. Save it in your project root folder (same folder as app.py)")
        print("3. Run this script again: python remove_white_background.py")
        print("\nOr:")
        print("- Change the 'input_image' variable in the script to match your filename")
        
    except Exception as e:
        print(f"❌ Error processing image: {e}\n")
        print("Make sure you have required libraries installed:")
        print("   pip install Pillow numpy")