# Evaluation Instructions

This evaluation is based on [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness).

---

## 1. Setup

Clone the repository and prepare the dataset:

```bash
git clone https://github.com/EleutherAI/lm-evaluation-harness.git
```

Add the `aime` dataset folder to the tasks directory:

```
lm-evaluation-harness/lm_eval/tasks/aime
```

Install the required dependencies:

```bash
pip install -e .[vllm]
```

---

## 2. Running the Evaluation

Set the following environment variables (**replace placeholders with your values**):

```bash
export TASK_SAMPLE_LIMIT="10000000"
export TASK_LIST="aime24_nofigures_agg8"
export CACHE_DIR="<YOUR_CACHE_DIR>"
export RESULT_DIR="<YOUR_RESULT_DIR>"
export OPENAI_API_KEY="<YOUR_OPENAI_API_KEY>"
export PROCESSOR="gpt-4o-mini"

tag="<YOUR_EXPERIMENT_TAG>"
model_path="<HUGGINGFACE_MODEL_PATH>"  # e.g., sunyiyou/openr1_diverse_1k_lg
```

Run the evaluation command:

```bash
lm_eval \
  --output_path ${RESULT_DIR}/${tag} \
  --use_cache ${CACHE_DIR}/${tag} \
  --model vllm \
  --model_args pretrained=${model_path},dtype=float32,tensor_parallel_size=8 \
  --tasks ${TASK_LIST} \
  --limit ${TASK_SAMPLE_LIMIT} \
  --batch_size auto \
  --apply_chat_template \
  --log_samples \
  --gen_kwargs max_gen_toks=32768
```

**Note:** Make sure all placeholders (`<...>`) are filled correctly before execution.