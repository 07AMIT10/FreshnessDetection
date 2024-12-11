import streamlit as st
from vertexai.generative_models import Part
import io
import re
import time
from datetime import datetime

def create_prompt_template():
    return """Analyze this image of produce (fruits/vegetables) and provide:

1. Produce Identification:
   Identify the specific fruit or vegetable shown.

2. Freshness Assessment (1-10 scale):
   Evaluate visual indicators including color, texture, blemishes. Vegetables tend to stay fresh for longer periods of time, so a higher score is expected.

3. Expected Shelf Life:
   Predict remaining days of freshness.
   
4. Confidence Score:
   Provide reliability percentage of assessment.

5. Visual Indicators Observed:
   List key visual cues used in assessment.

Present results in this format:
Produce: [name]
Freshness Score: [1-10]
Expected Lifespan (Days): [number]
Confidence Score: [percentage]
Key Indicators: [bullet points]"""

def parse_analysis_response(response_text):
    details = {
        "Sl No": len(st.session_state.produce_data) + 1,
        "Timestamp": datetime.now().astimezone().isoformat(),
        "Produce": "Not specified",
        "Freshness": 0,
        "Expected Lifespan (Days)": 0,
        "Visual Indicators": []
    }
    
    current_section = None
    
    for line in response_text.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('Produce:'):
            details["Produce"] = line.split(':', 1)[1].strip()
        elif line.startswith('Freshness Score:'):
            score = line.split(':', 1)[1].strip()
            details["Freshness"] = int(score) if score.isdigit() else 0
        elif line.startswith('Expected Lifespan'):
            lifespan = line.split(':', 1)[1].strip()
            match = re.search(r'(\d+)', lifespan)
            details["Expected Lifespan (Days)"] = int(match.group(1)) if match else 0
        elif line.startswith('Key Indicators:'):
            current_section = "Indicators"
        elif current_section == "Indicators" and line.startswith('-'):
            details["Visual Indicators"].append(line.lstrip('- '))
    
    return details

def analyze_image(image):
    try:
        start_time = time.time()
        
        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        prompt = create_prompt_template()
        
        # Access model from session state
        model = st.session_state.model
        
        # Create proper Part object
        image_part = Part.from_data(img_byte_arr, mime_type="image/png")
        
        # Send both prompt and image as parts
        response = model.generate_content(
            [prompt, image_part],
            generation_config={
                "max_output_tokens": 1024,
                "temperature": 0.1,
                "top_p": 1,
                "top_k": 32
            }
        )
        
        analysis = parse_analysis_response(response.text)
        current_time = datetime.now().astimezone().isoformat()
        analysis['timestamp'] = current_time
        
        return analysis
        
    except Exception as e:
        st.error("Error analyzing image")
        return None
