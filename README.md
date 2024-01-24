# rca_apriori_bayesian

## 项目简介
`rca_apriori_bayesian` 是一个采用关联规则挖掘和贝叶斯网络实现根因分析的项目。在复杂的信息技术环境中，系统的稳定性和可靠性至关重要。本项目基于 CMDiagnostor 论文提出的模块化根因分析方法，通过结合关联规则挖掘和贝叶斯网络，实现了对系统故障的快速准确定位。其模块化设计使得各阶段可以独立运作，便于根据特定场景进行调整和优化。

## 安装指南

### 软件环境

- **开发环境**：PyCharm专业版
- **操作系统**：Windows
- **编程语言**：Python

### 依赖库

- `mlxtend`
- `pyrca`

### 安装步骤

请在 Python 环境下安装所需的依赖库。可以使用 pip 命令来安装：

```bash
pip install mlxtend pyrca
```

## 使用说明

要运行项目，请直接运行 main 函数。确保 `data` 文件夹下有历史告警数据。

## 功能和优势

- **关联规则与贝叶斯网络的结合**：使用 Apriori 算法产生的关联规则作为贝叶斯网络训练数据，提高根因分析的准确性。
- **非明确调用关系的分析**：有效处理没有明显调用关系的服务或组件，通过告警数据的时间序列挖掘潜在因果关系。
- **实际应用中的实用性**：理论创新与实际应用相结合，显示出更广泛的适用性和有效性。

## 输入输出格式

**输入格式**

输入数据应为 JSON 格式，包含以下关键字段：

- `id`, `create_time`, `type`
- `resource`, `resource_id`
- `description`, `status`
- `duplicate_count`, `metadata`
- `severity_score`

**输出格式**

输出结果包括：

- 根因节点和路径
- 概率评分和可能的根因链
- 示例输出：

```json
{
  "root_cause_nodes": [...],
  "root_cause_paths": {...}
}

```

