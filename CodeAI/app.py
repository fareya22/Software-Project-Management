"""
Streamlit UI for AI Code Generator and CodeBLEU Evaluator
"""

import os
from typing import Optional

import streamlit as st

# Try to load .env if present
try:
	st.set_page_config(page_title="AI Code Generator & Evaluator", page_icon="💻", layout="wide")
	from dotenv import load_dotenv
	load_dotenv()
except Exception:
	pass

from code_generator import CodeGenerator
from code_evaluator import CodeBLEUEvaluator


@st.cache_resource(show_spinner=False)
def get_services(api_key: Optional[str], model: str):
	return CodeGenerator(api_key=api_key, model=model), CodeBLEUEvaluator()


LANG_TO_EXT = {
	"python": "py",
	"cpp": "cpp",
	"java": "java",
	"javascript": "js",
	"typescript": "ts",
	"go": "go",
	"rust": "rs",
}


def main():
	st.title("AI Code Generator and Evaluator")
	st.caption("Generate code from natural language and evaluate correctness with CodeBLEU")

	rerun_func = getattr(st, "rerun", None)
	if rerun_func is None:
		rerun_func = getattr(st, "experimental_rerun", None)

	# Initialize session state
	default_language = "python"
	for key, default in {
		"query_input": "",
		"reference_code_input": "",
		"generated_code": "",
		"evaluation_results": None,
		"language_select": default_language,
		"filename_input": f"generated_code.{LANG_TO_EXT.get(default_language, 'txt')}",
		"last_language_for_filename": default_language,
	}.items():
		st.session_state.setdefault(key, default)

	# Handle pending reset request before widgets render
	if st.session_state.get("reset_chat_flag"):
		st.session_state["query_input"] = ""
		st.session_state["reference_code_input"] = ""
		st.session_state["generated_code"] = ""
		st.session_state["evaluation_results"] = None
		current_lang = st.session_state.get("language_select", default_language)
		st.session_state["filename_input"] = f"generated_code.{LANG_TO_EXT.get(current_lang, 'txt')}"
		st.session_state["last_language_for_filename"] = current_lang
		st.session_state["reset_chat_flag"] = False
		if rerun_func:
			rerun_func()
		return

	with st.sidebar:

		def _on_language_change():
			lang = st.session_state["language_select"]
			ext = LANG_TO_EXT.get(lang, "txt")
			prev_lang = st.session_state.get("last_language_for_filename", default_language)
			prev_default = f"generated_code.{LANG_TO_EXT.get(prev_lang, 'txt')}"
			current = st.session_state.get("filename_input", "")
			if not current or current == prev_default:
				st.session_state["filename_input"] = f"generated_code.{ext}"
			st.session_state["last_language_for_filename"] = lang

		st.header("Settings")
		api_key = st.text_input(
			"Mistral API Key",
			type="password",
			value=os.getenv("MISTRAL_API_KEY") or "",
			help="Stored only for this session. Or set MISTRAL_API_KEY in your .env",
		)
		model = st.selectbox(
			"Model",
			options=["codestral-latest", "codestral-mamba-latest"],
			index=0,
		)
		language = st.selectbox(
			"Target language",
			options=list(LANG_TO_EXT.keys()),
			index=list(LANG_TO_EXT.keys()).index(st.session_state["language_select"]),
			key="language_select",
			on_change=_on_language_change,
		)
		st.text_input(
			"Optional output filename",
			key="filename_input",
		)
		generate_btn = st.button("Generate Code", type="primary")
		if st.button("New Chat"):
			st.session_state["reset_chat_flag"] = True
			if rerun_func:
				rerun_func()
			return

	col_input, col_output = st.columns([5, 7], vertical_alignment="top")

	with col_input:
		st.subheader("Prompt")
		query = st.text_area(
			"Describe what code you want",
			placeholder="Create a Python function to calculate factorial",
			height=160,
			key="query_input",
		)

		st.subheader("Optional: Reference Code for Evaluation")
		reference_code = st.text_area(
			"Paste correct/reference code to evaluate against (optional)",
			placeholder="def factorial(n):\n\treturn 1 if n <= 1 else n * factorial(n-1)",
			height=160,
			key="reference_code_input",
		)
		evaluate_btn = st.button("Generate and Evaluate")

	with col_output:
		st.subheader("Generated Code")
		code_container = st.empty()
		download_container = st.empty()

	generated_code = st.session_state.get("generated_code")
	eval_results = st.session_state.get("evaluation_results")

	if generate_btn or evaluate_btn:
		if not api_key:
			st.error("Mistral API key is required. Add it in the sidebar.")
			return
		if not query.strip():
			st.error("Please enter a prompt.")
			return

		try:
			generator, evaluator = get_services(api_key, model)
			code = generator.generate_code(query=query, language=language)
			st.session_state["generated_code"] = code
			st.session_state["evaluation_results"] = None

			if evaluate_btn and reference_code.strip():
				results = evaluator.evaluate(code, reference_code, language=language)
				st.session_state["evaluation_results"] = results

		except Exception as e:
			st.error(f"Error: {e}")
			return

		# refresh to display new state
		if rerun_func:
			rerun_func()

	# display stored code/results
	if generated_code:
		code_container.code(generated_code, language=language)

		current_filename = st.session_state.get("filename_input", "").strip()
		if current_filename:
			download_container.download_button(
				label="Download code",
				data=generated_code.encode("utf-8"),
				file_name=current_filename,
				mime="text/plain",
			)

	if eval_results:
		st.subheader("Evaluation")
		col1, col2, col3, col4, col5 = st.columns(5)
		with col1:
			st.metric("CodeBLEU", f"{eval_results['codebleu']:.3f}")
		with col2:
			st.metric("BLEU", f"{eval_results['bleu']:.3f}")
		with col3:
			st.metric("Syntax", f"{eval_results['syntax_match']:.3f}")
		with col4:
			st.metric("Dataflow", f"{eval_results['dataflow_match']:.3f}")
		with col5:
			st.metric("AST", f"{eval_results['ast_match']:.3f}")

		if eval_results.get("is_correct"):
			st.success("Correct according to threshold")
		else:
			st.info("Thanks for evaluating the code!")


if __name__ == "__main__":
	main()