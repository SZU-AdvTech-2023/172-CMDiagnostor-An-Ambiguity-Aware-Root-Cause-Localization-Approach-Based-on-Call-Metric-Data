def extract_root_cause_info(result):
    root_cause_info = {
        "Root Cause": None,
        "Root Cause Chains": []
    }

    for path in result['root_cause_paths'].values():
        for score, chain in path:
            # 提取 Root Cause
            root_cause_node, root_cause_prob = chain[-1]
            root_cause_info["Root Cause"] = f"{root_cause_node.split('_')[-1]} (Probability: {root_cause_prob})"

            # 构建并添加 Root Cause Chain
            chain_description = " -> ".join([f"{node.split('_')[-1]} ({prob})" for node, prob in chain[::-1]])
            root_cause_info["Root Cause Chains"].append(f"Root Cause Chain: {chain_description}")

    return root_cause_info

def main():
    original_result = {
        'root_cause_nodes': [('ROOT_饼干', 0.99)],
        'root_cause_paths': {
            'ROOT_饼干': [
                (0.9933333333333333, [('ROOT_饼干', 0.99), ('饼干', 1), ('牛奶', 0.99)]),
                (0.8283333333333334, [('ROOT_饼干', 0.99), ('饼干', 1), ('面包', 0.3333333333333333), ('牛奶', 0.99)])
            ]
        }
    }

    root_cause_info = extract_root_cause_info(original_result)
    print("Root Cause:")
    print(root_cause_info["Root Cause"])
    print("\nRoot Cause Chains:")
    for chain in root_cause_info["Root Cause Chains"]:
        print(chain)

if __name__ == "__main__":
    main()
