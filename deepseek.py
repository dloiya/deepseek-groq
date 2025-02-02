import streamlit as st
import groq
import re

def fetch_pubmed_articles(query):
    api_key = "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"
    groq_client = groq.Client(api_key=api_key) if api_key else None
    messages = [{"role": "user", "content": query}]

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=7500
    )

    return response.choices[0].message.content

def main():
    st.title("Deepseek 🐋")

    # Larger input text area
    query = st.text_area(
        "Enter your search query:",
        "",
        key="query_input",
        help="Type your query here.",
        max_chars=None,  # Allows for longer input
    )

    if st.session_state.get('summaries', None) is None:
        st.session_state.summaries = []

    with st.expander("Previous Summaries"):
        for i, summary in enumerate(st.session_state.summaries):
            st.write(f"**Summary {i+1}**")

            # Remove hidden sections from the summary
            hidden_sections = re.findall(r"(((Hidden content available)))", summary, re.DOTALL)
            for section in hidden_sections:
                summary = summary.replace(section, "(((Hidden content available)))", 1)

            st.markdown(summary)

            # Show hidden sections on button click
            show_hidden = st.checkbox("Show Hidden Thoughts", key=f"show_hidden_{i}")
            if show_hidden:
                for section in hidden_sections:
                    st.markdown(section)

            # Handle LaTeX equations
            latex_expressions = re.findall(r'\$(.*?)\$', summary)
            for expr in latex_expressions:
                st.latex(expr)

            # Handle code blocks
            code_blocks = re.findall(r'```(.*?)```', summary, re.DOTALL)
            for code in code_blocks:
                st.code(code, language="python")
                st.button("Copy to Clipboard", key=f"copy_{hash(code)}")
                st.write("------------------------")

    if st.button("Fetch"):
        if query:
            with st.spinner("Fetching..."):
                summary = fetch_pubmed_articles(query)

                # Remove hidden sections from the summary
                hidden_sections = re.findall(r"<think>(.*?)</think>", summary, re.DOTALL) 
                for section in hidden_sections:
                    summary = summary.replace(f"<think>{section}</think>", "(((Hidden content available)))", 1)


                # Display formatted output
                st.markdown(summary)

                # Show hidden sections on button click
                show_hidden = st.checkbox("Show Hidden Thoughts")
                if show_hidden:
                    for section in hidden_sections:
                        st.markdown(section)

                # Handle LaTeX equations
                latex_expressions = re.findall(r'\$(.*?)\$', summary)
                for expr in latex_expressions:
                    st.latex(expr)

                # Handle code blocks
                code_blocks = re.findall(r'```(.*?)```', summary, re.DOTALL)
                for code in code_blocks:
                    st.code(code, language="python")
                    st.button("Copy to Clipboard", key=f"copy_{hash(code)}")

                # Append the summary to the list of summaries
                st.session_state.summaries.append(summary)
        else:
            st.error("Please enter a search query.")
        st.button("Clear Summaries", key="clear_summaries", on_click=lambda: st.session_state.summaries.clear())
if __name__ == "__main__":
    main()