# 📅 Schedule App

## 🚀 Description
Schedule App is an algorithm designed to efficiently organize academic subjects and their corresponding schedules. Given a set of subjects, their priority, and time availability, the system generates multiple optimized schedule variations for users to choose from.

## 📝 Features
- 📄 **PDF Integration:** Automatically extract subject and schedule data from university-provided PDFs.
- 🖊️ **Manual Input:** Manually input subjects and their details.
- ⚙️ **Priority Organization:** Sorts subjects by relevance and priority.
- 📊 **Schedule Variations:** Generates up to 5 optimized schedule variations.
- 📑 **Export Options:** Export schedules in PDF or CSV formats.

## 📥 Inputs
### Subjects
- **Relevance Level**
- **Name**
- **Credits**
- **Groups**
- **Weekly Schedule per Group**

## 📤 Outputs
- Optimized **Schedule Variations**
- Export as **PDF** or **CSV**

## 🔄 Process
1. **Data Input:** User manually inputs subjects or uploads a PDF.
2. **Data Extraction:** System extracts and processes subject details.
3. **Priority Organization:** Subjects are sorted by priority.
4. **Schedule Generation:** The system generates up to 3 schedule variations.
5. **Export:** The final schedule can be exported as PDF or CSV.

## 📚 Data Structures
### Schedule
```json
{
  id: int,
  subjects: [] int
}
```
### Subject
```json
{
  id: int,
  name: string,
  priority: int,
  credits: int,
  groups_id: [] int
}
```
### Group
```json
{
  id: int,
  schedule_date1: Datetime,
  duration_schedule1: int,
  schedule_date2: Datetime,
  duration_schedule2: int
}
```

## 🧠 Algorithm
### Data Reading
```python
subjects = read_data()
```
- `read_data` extracts data from PDF or manual input and converts it into structured `Subject` objects.

### Schedule Generation
```python
schedule.subjects = subjects
schedule.generate_variations()
```
- `generate_variations` generates up to 3 optimal schedule combinations.

## 📦 Installation
1. Clone the repository:
```bash
git clone https://github.com/SSAYKO/schedule_app.git
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the application:
```bash
python main.py
```

## 🤝 Contributing
Feel free to fork this repository and submit pull requests.

## 📄 License
This project is licensed under the MIT License.

## 🌐 Repository
[GitHub - SSAYKO/schedule_app](https://github.com/SSAYKO/schedule_app.git)

---
by **SSAYKO**
