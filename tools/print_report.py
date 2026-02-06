import sys
import json


def print_summary(public_report_path):
    try:
        with open(public_report_path, 'r') as f:
            data = json.load(f)

        print("\n" + "="*60)
        print("SECURE RAG: VERIFICATION SUMMARY")
        print("="*60)
        print(f"Dataset Used:      {data['dataset']}")
        print(f"Sample Size:       {data['samples']} pairs")
        print(f"Embedding Model:   {data['model']}")
        print("-" * 60)
        print(f"Retrieval Accuracy: {data['accuracy']}%")
        print(f"System Status:      {data['status']}")
        print("="*60 + "\n")

    except Exception as e:
        print(f"Error reading report: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print_summary(sys.argv[1])
