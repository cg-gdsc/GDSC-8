# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Global Data Science Challenge 8 (GDSC-8): **Green Agents of Change** lead by Capgemini. 

**Partnership**: UNICEF and Mistral AI
**Focus**: Empowering youth across Brazil to explore and pursue green and future-proof jobs
**Goal**: Build AI agents that match young people with sustainable careers by analyzing job descriptions and training opportunities

The challenge involves:
- Interacting with persona agents via AWS API endpoints
- Processing job and training data from local files or AWS S3
- Creating intelligent matching algorithms based on skills, constraints, and preferences
- Optimizing for both accuracy and resource efficiency (green computing)

## Development Commands

### Package Management
- **Install dependencies**: `uv sync` or `uv pip install -r pyproject.toml`
- **Add new dependency**: `uv add <package>`
- **Run Python scripts**: `uv run python <script.py>`

### Jupyter Notebooks
- **Start Jupyter**: `uv run jupyter lab` or `uv run jupyter notebook`
- **Main notebooks are in**: `tutorials/` directory

## Data Architecture

### Data Sources
1. **Personas**: Fictional beneficiaries as Mistral agents on AWS API endpoints
2. **Jobs**: 200 job descriptions in `data/jobs/` (markdown format with JSON structure)
3. **Trainings**: 467 training programs in `data/trainings/` (markdown format with JSON structure)

### Data Schemas

#### Persona Schema
```json
{
  "id": "pers_001",
  "domain_focus": "Marketing",
  "age": 25,
  "education_level": "Bachelor's Degree",
  "years_experience": 2,
  "current_role": "Communications Officer",
  "skills": [{"name": "SEO", "level": 3}, {"name": "Copywriting", "level": 2}],
  "interests": [{"name": "Brand strategy", "weight": 0.7}, {"name": "Data analytics", "weight": 0.3}],
  "constraints": {"location": "Paris", "mobility": "low", "contract": "Permanent"},
  "reason_for_consult": "Wants to move into a marketing project manager role",
  "expected_output_type": "jobs"
}
```
- **Skill levels**: 0-4 scale (0=none, 4=expert)
- **Constraints**: location, mobility, contract type, language, working hours, seniority, age

#### Job Schema
```json
{
  "id": "job_001",
  "domain": "Marketing",
  "title": "Digital Marketing Project Manager",
  "seniority": "mid-level",
  "required_skills": [{"name": "SEO", "min_level": 3}, {"name": "Project Management", "min_level": 2}],
  "nice_to_have": [{"name": "HTML", "min_level": 1}],
  "location": "Paris",
  "contract": "Permanent",
  "tasks": ["Coordinate digital campaigns", "Analyze KPIs"],
  "salary_band": "35-45k€",
  "language": "FR"
}
```

#### Training Schema
```json
{
  "id": "tr_001",
  "domain": "Marketing",
  "title": "Digital Project Management Training",
  "outcomes": [{"name": "Project Management", "target_level": 3}, {"name": "SEO", "target_level": 4}],
  "prerequisites": [{"name": "Project Management", "min_level": 1}],
  "duration_weeks": 8,
  "format": "online",
  "language": "FR",
  "certification": true
}
```

## Matching Rules

### Hard Filters (Automatic Disqualification)
- Insufficient seniority level
- Location/mobility incompatibility
- Required language not mastered
- Domain mismatch (if `domain_lock: true`)
- Contract type or working hours mismatch

### Skill Coverage Calculation
```
coverage = (# required skills satisfied) / (total required skills)
```
- Skill satisfied if: `persona_level ≥ job_min_level`
- Job compatible if: `coverage ≥ 0.70` after passing hard filters

## Output Types

### Case 1: Jobs
- For personas seeking employment
- Apply hard filters and 70% skill coverage rule
- Include training suggestions for skill gaps

### Case 2: Trainings
- For personas explicitly seeking training
- Match training programs to learning objectives

### Case 3: Awareness
- For minors (<16) or general information seekers
- No specific recommendations required

### Expected Output Format
```json
{"persona_id": "pers_001", "gold_type": "jobs+trainings", "jobs": [{"job_id": "job_001", "suggested_trainings": ["tr_001"]}]}
{"persona_id": "pers_002", "gold_type": "trainings_only", "trainings": ["tr_002", "tr_003"]}
{"persona_id": "pers_003", "gold_type": "awareness", "gold_items": "too_young"}
```

## Key Dependencies
- **strands-agents[mistral]**: Agent framework with Mistral integration
- **python-dotenv**: Environment variable management
- **Python 3.11+**: Required runtime

## Evaluation Criteria & Scoring Function

### How Scoring Works (from eval/evaluate_all.py)

The evaluation system calculates your score based on two main components:

1. **Type Accuracy (50% of score)**
   - Did you correctly identify whether the persona needs `jobs+trainings`, `trainings_only`, or `awareness`?
   - Binary: either correct (1.0) or wrong (0.0)
   - For awareness cases: includes minors (<16) who should get `predicted_items: "too_young"`

2. **Recommendation Accuracy (50% of score)**
   - How well did your specific recommendations match the gold standard?
   - Calculated differently per type:

   **For `jobs+trainings`:**
   - Job matching F1 score (50% of RecoScore)
   - Training suggestions per job F1 score (50% of RecoScore)
   - Formula: `RecoScore = 0.5 * F1_Jobs + 0.5 * F1_TrainingsPerJob`

   **For `trainings_only`:**
   - F1 score between predicted and gold training sets
   - Formula: `RecoScore = F1_Trainings`

   **For `awareness`:**
   - Exact match on reason (e.g., "too_young", "info_request")
   - Formula: `RecoScore = 1.0 if reasons match else 0.0`

3. **Final Score Calculation**
   ```
   FinalScore = 0.5 * TypeAccuracy + 0.5 * RecoMacro
   ```
   Where RecoMacro is the average RecoScore across all personas

### Important Notes for Scoring
- Type mismatch = 0 RecoScore (even if recommendations are good)
- Missing the awareness type for minors is leaving easy points on the table
- Training suggestions matter! They're 25% of your score for jobs+trainings type
- The evaluator normalizes field names (e.g., `predicted_type` and `gold_type` both work)

## Tutorial Author Guidelines

When creating tutorials for GDSC 8, follow these style guidelines:

### Writing Style
- **Natural, dev-to-dev tone**: Write like a senior developer explaining to colleagues
- **Keep it real**: Acknowledge TODOs, costs, competitive aspects honestly
- **Conversational language**: "Let's get our hands dirty" not "Welcome to Module X!"
- **Practical focus**: "and not go broke doing it" instead of polished consulting speak
- **Geek-friendly**: Assume participants are smart and motivated
- **Authentic**: It's okay to say "this is tricky" or "we don't know the exact pricing yet"
- **Human**: We're consultants AND competitors AND geeks - embrace all aspects

### Key Themes
- Frame everything through **modern consulting skills** - balancing capability, cost, and environmental impact
- Show how LLMs have transformed solution development but require strategic thinking
- Emphasize the **green computing** aspect - optimal resource usage matters

### Tutorial Requirements
- **Learning Objectives**: Clearly define what participants should achieve
- **References**: Include links to relevant documentation and examples
- **Exercises**: Add both simple and advanced exercises
- **Support Reminder**: Encourage Teams channel participation and office hours

## Reference Documentation

### Tutorial Specifications
- **Tutorial Details**: See `docs/tutorial-specifications.md` for complete tutorial structures and author notes
- **GDSC 7 Examples**: See `docs/gdsc7-examples.md` for detailed implementation examples from last year

### When Working on Tutorials
1. Read the tutorial specifications in `docs/tutorial-specifications.md` for your specific tutorial
2. Follow the author guidelines above for tone and style
3. Reference GDSC 7 examples for implementation patterns but adapt to GDSC 8's green jobs focus
4. Test all code examples with actual Mistral API calls and cost calculations