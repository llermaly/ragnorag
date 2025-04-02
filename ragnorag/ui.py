import streamlit as st
from es import ask
from annotated_text import annotated_text

def highlight_answer_in_section(section_text, answer):
    """Highlight the answer within the section text using annotated_text"""
    before, after = section_text.split(answer, 1)
    
    # Return the text with the answer annotated
    return annotated_text(
        before,
        (answer, "", "rgb(22 97 50)"),
        after
    )


def main():
    st.title("NonRAG Q&A System")
    question = st.text_input("Ask a question about Lionel Messi:")

    if question:
        try:
            # Get response from elasticsearch
            result = ask(question)

            if result and "section" in result:
                section = result["section"]
                answer = result["answer"]

                # Display article metadata
                col1, col2 = st.columns([1, 2])

                with col1:
                    st.image(
                        section["image_url"],
                        caption=section["title"],
                        use_container_width=True,
                    )

                with col2:
                    st.header(section["title"])
                    st.write(f"From section: {section['section_name']}")
                    st.write(f"[Read full article]({section['wiki_link']})")

                # Display the answer
                st.subheader("Answer:")
                st.markdown(answer)

                # Add toggle button for full context
                on = st.toggle("Show context")

                if on:
                    st.subheader("Full Context:")
                    # Now using annotated_text instead of markdown
                    highlight_answer_in_section(
                        section["content"], answer
                    )

            else:
                st.error("Sorry, I couldn't find a relevant answer to your question.")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.error("Please try again with a different question.")


if __name__ == "__main__":
    main()
