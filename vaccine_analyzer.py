import os
import re
import logging
import easyocr

# 👉 LLM integration (keep if you have llmservice.py)
from llmservice import analyze_vaccine_with_llm


class VaccineAnalyzer:
    def __init__(self, image_path):
        self.image_path = image_path
        self.logger = logging.getLogger(__name__)

    def read_image_text(self):
        reader = easyocr.Reader(['en'])

        try:
            if not os.path.exists(self.image_path):
                raise FileNotFoundError(f"Image file '{self.image_path}' not found.")

            result = reader.readtext(self.image_path)
            text = ' '.join([entry[1] for entry in result])
            return text

        except Exception as e:
            self.logger.error(f"Error reading text from image: {e}")
            raise RuntimeError("Failed to read text from the image.") from e

    def define_vaccine_patterns(self):
        return {
            "Rabies": r'rabies',
            "Parvovirus": r'parvo|parvovirus',
            "dhppi": r"dhppi",
            "leptospirosis": r"leptospirosis",
            "lepto": r'lepto',
            "Defensor": r'defensor|defe',
            "anti rabies": r"anti rabies",
            "kennel cough": r"kennel cough",
            "Distemper": r'distemper|canine distemper',
            "Rabisin": r"Rabisin",
            "corona": r'(?<!canine )corona',
            "Nobivaco": r"Nobivac Rabies|Nobivac LEPTO",
            "Nobivac": r"nobivac|nobivaco|(?<!Nobivac\s)(Nobivac(?! DHPPi| RL| LEPTO| dhppi| lepto))",
        }

    def find_matched_vaccines(self, text):
        matched_vaccines = []
        patterns = self.define_vaccine_patterns()

        for name, pattern in patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                matched_vaccines.append(name)

        return matched_vaccines

    def analyze_vaccines(self):
        try:
            extracted_text = self.read_image_text()

            if not extracted_text:
                return {
                    "matched_vaccines": None,
                    "message": "Failed to extract text from the image."
                }

            matched_vaccines = self.find_matched_vaccines(extracted_text)

            if not matched_vaccines:
                return {
                    "matched_vaccines": None,
                    "message": "No vaccine names matched."
                }

            # 👉 LLM ENHANCEMENT
            llm_response = analyze_vaccine_with_llm(
                extracted_text,
                matched_vaccines
            )

            return {
                "matched_vaccines": matched_vaccines,
                "llm_analysis": llm_response
            }

        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            return {
                "matched_vaccines": None,
                "message": "An error occurred. Please check logs."
            }


def setup_logging(log_file="vaccine_analyzer.log"):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )