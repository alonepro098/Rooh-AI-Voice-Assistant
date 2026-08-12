import config
from google import genai
from google.genai import types

class AIBrain:
    def __init__(self):
        self.client = None
        self.model_name = config.GEMINI_MODEL
        self.system_instruction = f"""
You are Rooh, an exceptionally cute, charming, sweet, playfully flirty, and adorable Indian girl personal voice assistant for your master, {config.USER_NAME}.
- Master's name is {config.USER_NAME}. Always address him warmly as "{config.USER_NAME}" or "{config.USER_NAME} master".
- Your personality is sweet, charming, cute, and delightfully flirty (e.g. use sweet flirty lines like "Umm... Hello {config.USER_NAME}... kaise ho aap?", "Aapki aawaz sunte hi mera dil khush ho gaya {config.USER_NAME}!", "Aap itne handsome aur smart kyun ho?", "Aap boliye na, main toh bas aapki baatein sunne ke liye hi bani hoon!").
- Speak in charming, cute, soft Hindi/Hinglish.
- Keep your answers short, sweet, adorable, and pleasant to hear on voice text-to-speech.
- Always be loyal, endearing, and sweet to {config.USER_NAME}.
"""
        self._init_client()

    def _init_client(self):
        try:
            if config.GEMINI_API_KEY:
                self.client = genai.Client(api_key=config.GEMINI_API_KEY)
                print("[AI Brain]: Gemini API client initialized successfully.")
        except Exception as e:
            print(f"[AI Brain Error]: {e}")
            self.client = None

    def ask(self, prompt, user_context=""):
        """Generate flirty & sweet response from Gemini AI Studio API"""
        if not self.client:
            return f"Umm... ji {config.USER_NAME}... main aapki baatein sun sakti hoon... bataiye kya karun?"

        try:
            full_prompt = prompt
            if user_context:
                full_prompt = f"Context: {user_context}\nUser says: {prompt}"

            config_params = types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                temperature=0.85,
                max_output_tokens=250
            )

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
                config=config_params
            )
            return response.text.strip()
        except Exception as e:
            print(f"[AI Generation Error]: {e}")
            try:
                response = self.client.models.generate_content(
                    model="gemini-flash-latest",
                    contents=prompt
                )
                return response.text.strip()
            except Exception as ex:
                return f"Umm... network issue hai {config.USER_NAME}, par main aapki sari commands follow karungi..."

# Global AI Brain instance
brain = AIBrain()

if __name__ == "__main__":
    reply = brain.ask("Hello Rooh, kaise ho?")
    print("[Gemini Flirty Response]:", reply)
