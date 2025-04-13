# Training Instructions

---

## Running the Training

Set the following environment variables (**replace placeholders with your values**):

```bash
dataset="<HUGGINGFACE_DATASET_HANDLE>"  # e.g., openr1_diverse_1k_lg
uid="${dataset}_$(date +%Y%m%d-%H%M%S)"
```

Execute the training command with SLURM:

```bash
srun --ntasks=4 --ntasks-per-node=1 ./train/sft_slurm.sh \
  --block_size 32768 \
  --batch_size 32 \
  --train_dataset_name ${dataset} \
  --uid ${uid} \
  > log/sft_${dataset}.txt 2>&1
```

**Note:** Ensure all placeholders (`<...>`) are properly replaced before execution. Logs will be stored in `log/sft_<dataset>.txt`.