MODEL_NAME="meta-llama/Llama-4-Scout-17B-16E-Instruct"
vllm serve $MODEL_NAME \
    --tensor-parallel-size 4 \
    --max-model-len 8192