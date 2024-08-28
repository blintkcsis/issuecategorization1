import streamlit as st
import requests
from openai import OpenAI
import os
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()
    api_key = os.getenv('API_KEY')
    client = OpenAI(api_key=api_key)
    st.title("Bee wise kategorizálás")

    # Dropdown for model selection
    model_options = {
        "Legjobb": "ft:gpt-4o-2024-08-06:ef-hackathon-london-5::A1BaEBWI",
        "Kicsi": "ft:gpt-4o-mini-2024-07-18:ef-hackathon-london-5::A1BLqEIV",
        "Régi": "ft:gpt-4o-2024-08-06:ef-hackathon-london-5::A0tGlKOA"
    }
    selected_label = st.selectbox("Válassz kategorizálót:", list(model_options.keys()))
    selected_model = model_options[selected_label]

    # Text input
    user_input = st.text_area("Hiba üzenet:", height=200)

    # Submit button
    if st.button("Küldés"):
        if user_input:
            try:
                completion = client.chat.completions.create(
                    model=selected_model,
                    messages=[
                        {"role": "system", "content": "A feladata hogy eldöntse a hibabejelentés alapján a bejelentési osztályt. Semmi mást."},
                        {"role": "user", "content": user_input}
                    ],
                )
                response = completion.choices[0].message
                # Display the response
                st.success("Elküldve!")
                st.subheader("Javaslat:")
                st.write(response.content)
            except Exception as e:
                st.error(f"Hiba történt: {str(e)}")
        else:
            st.warning("Nincs hibaüzenet hozzáadva.")

if __name__ == "__main__":
    main()