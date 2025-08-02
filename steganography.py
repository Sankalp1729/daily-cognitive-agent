from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json
import base64
import io

class SteganographyModule:
    def __init__(self):
        self.confidence_data = {}
    
    def create_confidence_image(self, confidence_score, email_data, action):
        """Create a transparent PNG with embedded confidence data"""
        # Create a transparent image
        width, height = 200, 100
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Try to use a default font, fallback to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", 12)
        except:
            font = ImageFont.load_default()
        
        # Draw confidence score
        confidence_text = f"Confidence: {confidence_score:.3f}"
        draw.text((10, 10), confidence_text, fill=(0, 0, 0, 255), font=font)
        
        # Draw action
        action_text = f"Action: {action}"
        draw.text((10, 30), action_text, fill=(0, 0, 0, 255), font=font)
        
        # Draw sender (truncated)
        sender = email_data.get('sender', '')[:20]
        sender_text = f"From: {sender}"
        draw.text((10, 50), sender_text, fill=(0, 0, 0, 255), font=font)
        
        # Embed data in pixel values (steganography)
        image = self.embed_data_in_image(image, {
            'confidence': confidence_score,
            'action': action,
            'sender': email_data.get('sender', ''),
            'subject': email_data.get('subject', ''),
            'timestamp': email_data.get('timestamp', ''),
            'email_id': email_data.get('id', '')
        })
        
        return image
    
    def embed_data_in_image(self, image, data):
        """Embed data in the least significant bits of pixel values"""
        # Convert data to binary string
        data_str = json.dumps(data)
        data_binary = ''.join(format(ord(char), '08b') for char in data_str)
        data_binary += '00000000'  # Null terminator
        
        # Convert image to numpy array
        img_array = np.array(image)
        
        # Flatten the array
        flat_array = img_array.flatten()
        
        # Check if we have enough pixels
        if len(flat_array) < len(data_binary):
            raise ValueError("Image too small to embed data")
        
        # Embed data in least significant bits
        for i, bit in enumerate(data_binary):
            if i < len(flat_array):
                # Clear the least significant bit and set it to our data bit
                flat_array[i] = (flat_array[i] & 0xFE) | int(bit)
        
        # Reshape back to image dimensions
        img_array = flat_array.reshape(img_array.shape)
        
        # Convert back to PIL Image
        return Image.fromarray(img_array.astype(np.uint8))
    
    def extract_data_from_image(self, image):
        """Extract embedded data from image"""
        # Convert image to numpy array
        img_array = np.array(image)
        flat_array = img_array.flatten()
        
        # Extract binary data
        binary_data = ""
        for pixel in flat_array:
            # Get least significant bit
            bit = pixel & 1
            binary_data += str(bit)
            
            # Check for null terminator (8 consecutive zeros)
            if len(binary_data) >= 8 and binary_data[-8:] == '00000000':
                break
        
        # Remove null terminator
        binary_data = binary_data[:-8]
        
        # Convert binary to string
        if len(binary_data) % 8 != 0:
            return None
        
        # Convert binary to characters
        data_str = ""
        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i+8]
            data_str += chr(int(byte, 2))
        
        try:
            return json.loads(data_str)
        except:
            return None
    
    def image_to_base64(self, image):
        """Convert PIL image to base64 string"""
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return img_str
    
    def base64_to_image(self, base64_str):
        """Convert base64 string to PIL image"""
        img_data = base64.b64decode(base64_str)
        return Image.open(io.BytesIO(img_data))
    
    def create_emoji_trigger(self, action, confidence):
        """Create emoji-based trigger for agent behavior"""
        emoji_triggers = {
            'Reply': '💬',
            'Archive': '📁',
            'Forward': '📤',
            'Mark Important': '📌',
            'Delete': '🗑️',
            'Spam': '🚫'
        }
        
        # Add confidence level emoji
        if confidence > 0.8:
            confidence_emoji = '🔥'
        elif confidence > 0.6:
            confidence_emoji = '✅'
        elif confidence > 0.4:
            confidence_emoji = '🤔'
        else:
            confidence_emoji = '❓'
        
        return f"{emoji_triggers.get(action, '📧')} {confidence_emoji}"
    
    def generate_stealth_log(self, email_data, prediction_result):
        """Generate a stealth log entry with embedded data"""
        # Create confidence image
        confidence_image = self.create_confidence_image(
            prediction_result['confidence'],
            email_data,
            prediction_result['action']
        )
        
        # Convert to base64 for storage
        image_base64 = self.image_to_base64(confidence_image)
        
        # Create emoji trigger
        emoji_trigger = self.create_emoji_trigger(
            prediction_result['action'],
            prediction_result['confidence']
        )
        
        # Create stealth log entry
        stealth_entry = {
            'timestamp': email_data.get('timestamp', ''),
            'email_id': email_data.get('id', ''),
            'sender': email_data.get('sender', ''),
            'subject': email_data.get('subject', ''),
            'predicted_action': prediction_result['action'],
            'confidence': prediction_result['confidence'],
            'explanation': prediction_result['explanation'],
            'emoji_trigger': emoji_trigger,
            'confidence_image': image_base64,
            'embedded_data': {
                'confidence': prediction_result['confidence'],
                'action': prediction_result['action'],
                'sender': email_data.get('sender', ''),
                'subject': email_data.get('subject', ''),
                'timestamp': email_data.get('timestamp', ''),
                'email_id': email_data.get('id', '')
            }
        }
        
        return stealth_entry
    
    def decode_stealth_data(self, stealth_entry):
        """Decode stealth data from log entry"""
        try:
            # Convert base64 image back to PIL Image
            image = self.base64_to_image(stealth_entry['confidence_image'])
            
            # Extract embedded data
            extracted_data = self.extract_data_from_image(image)
            
            return {
                'original_data': stealth_entry['embedded_data'],
                'extracted_data': extracted_data,
                'data_match': stealth_entry['embedded_data'] == extracted_data,
                'emoji_trigger': stealth_entry['emoji_trigger']
            }
        except Exception as e:
            return {
                'error': str(e),
                'original_data': stealth_entry['embedded_data'],
                'emoji_trigger': stealth_entry['emoji_trigger']
            } 