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

    # Settings dropdown
    with st.expander("Beállítások"):
        # Dropdown for model selection
        model_options = {
            "Legjobb": "ft:gpt-4o-2024-08-06:ef-hackathon-london-5::A1BaEBWI",
            "Kicsi": "ft:gpt-4o-mini-2024-07-18:ef-hackathon-london-5::A1BLqEIV",
            "Régi": "ft:gpt-4o-2024-08-06:ef-hackathon-london-5::A0tGlKOA"
        }
        selected_label = st.selectbox("Válassz kategorizálót:", list(model_options.keys()))
        selected_model = model_options[selected_label]

        # Confidence threshold slider
        confidence_threshold = st.slider("Magabiztosság minimum (%)", min_value=0, max_value=100, value=60, step=1)

    # Text input
    user_input = st.text_area("Hiba üzenet:", height=200)

    # Submit button
    if st.button("Küldés"):
        
        if user_input:
            try:
                
                

                if selected_model== "ft:gpt-4o-2024-08-06:ef-hackathon-london-5::A1BaEBWI":
        
                    completion = client.chat.completions.create(
                    model=selected_model,
                    messages=[
                        {"role": "system", "content": "A user a helyes bejelentési osztályt akarja tudni. A válaszok alapján döntse el melyik a helyes. (Amennyiben az assistant válaszai változékonyak, írja a válaszba hogy '- bizonytalan')"},
                        {"role": "user", "content": user_input},
                        {"role": "system", "content": "Válassz a következő listából: 'Damage repair activity', 'Electrical issue', 'Heating equipment', 'Water supply, wastewater management', 'Refrigeration equipment', 'Elevators', 'Windows and doors', 'Restrooms', 'Master builder (skilled trades) works', 'Move management, freight transport', 'Havaria', 'Catering areas', 'Furniture repair', 'Comfort improvement', 'Outdoor Maintenance ', 'Energy development', 'Havária - Víz és csatorna', 'Pest control', 'Occasional cleaning', 'Havaria - Electric', 'Havaria - Trailers', 'Havaria - Other emergency', 'Havaria - Garden and landscaping', 'Equipment replacement', 'Hygiene consumables', 'Other improvements', 'Support And Transport Activities', 'Carrying out design, expert and technical inspection tasks', 'Air conditioning and air handling equipment', 'Ceiling', 'Outdoor maintenance', 'Damage rescue, asset protection', 'Energy services', 'Caretaking', 'Main part replacement', 'Rationalization', 'Low-current services'"},
                            
                    ],
                    n=10
                    )

                    responses = [choice.message.content for choice in completion.choices]

                    # Count occurrences of each response
                    response_counts = {}
                    for resp in responses:
                        response_counts[resp] = response_counts.get(resp, 0) + 1
                    
                    # Find the most common response
                    most_common = max(response_counts, key=response_counts.get)
                    
                    # Check if the most common response occurs at least 6 times
                    if response_counts[most_common] >= int(confidence_threshold/10):
                        response = most_common
                    else:
                        st.error("Nem vagyok biztos a válaszban")
                        response = most_common

                    answer = response
                else:
                    response = client.chat.completions.create(
                    model=selected_model,
                    messages=[
                        {"role": "system", "content": "A user a helyes bejelentési osztályt akarja tudni. A válaszok alapján döntse el melyik a helyes. (Amennyiben az assistant válaszai változékonyak, írja a válaszba hogy '- bizonytalan')"},
                        {"role": "user", "content": user_input},
                        {"role": "system", "content": "Válassz a következő listából: 'Damage repair activity', 'Electrical issue', 'Heating equipment', 'Water supply, wastewater management', 'Refrigeration equipment', 'Elevators', 'Windows and doors', 'Restrooms', 'Master builder (skilled trades) works', 'Move management, freight transport', 'Havaria', 'Catering areas', 'Furniture repair', 'Comfort improvement', 'Outdoor Maintenance ', 'Energy development', 'Havária - Víz és csatorna', 'Pest control', 'Occasional cleaning', 'Havaria - Electric', 'Havaria - Trailers', 'Havaria - Other emergency', 'Havaria - Garden and landscaping', 'Equipment replacement', 'Hygiene consumables', 'Other improvements', 'Support And Transport Activities', 'Carrying out design, expert and technical inspection tasks', 'Air conditioning and air handling equipment', 'Ceiling', 'Outdoor maintenance', 'Damage rescue, asset protection', 'Energy services', 'Caretaking', 'Main part replacement', 'Rationalization', 'Low-current services'"},
                            
                    ],
                    n=1
                    )
                    answer = response.choices[0].message.content

                


                # Display the response
                st.success("Elküldve!")
                st.subheader("Javaslat:")
                st.write(answer)
                
            except Exception as e:
                st.error(f"Hiba történt: {str(e)}")
        else:
            st.warning("Nincs hibaüzenet hozzáadva.")

        

if __name__ == "__main__":
    main()