# CalmPulse: Backend Migration (Spring Boot & Cloud MongoDB)

This project has been migrated from a Python Flask backend to a structured **Spring Boot 3.x** Java application using **Cloud MongoDB** (via Spring Data MongoDB). The machine learning models remain integrated via a lightweight Python microservice.

---

## Project Architecture

```
Users (Browser)
      │
      ▼
HTML/CSS/JavaScript Frontend
      │
      ▼
Spring Boot REST API (Port 8080)
      │
 ┌────┴────────────────┐
 │                     │
 ▼                     ▼
Cloud MongoDB    Python ML Service (Port 5001)
                       │
                       ▼
                Trained ML Models (.pkl)
                       │
                       ▼
                  Gemini API
```

---

## Directory Structure

- **`Front end/`**: Contains HTML, CSS, and JS files. The `api-config.js` points to `http://localhost:8080` (Spring Boot).
- **`ML/`**: Contains Python machine learning models and the lightweight prediction microservice.
  - `prediction_service.py`: Lightweight prediction server (Flask) running on port `5001`.
  - `employee_model.pkl` & `student_model.pkl`: Serialized sklearn model files.
- **`backend/`**: Structured Spring Boot Maven project containing:
  - `pom.xml`: Maven configuration with Spring Boot 3.3.1, Spring Data MongoDB, Validation, Lombok, Security, and Swagger.
  - `src/main/resources/application.properties`: Configuration for database connection, ports, external service URLs, and logging.
  - `src/main/java/com/calmpulse/backend/`:
    - `config`: `SecurityConfig` (CORS & permit-all filter), `AppConfig` (RestTemplate & BCrypt beans).
    - `entity`: `User` and `StressHistory` mapping to MongoDB collections.
    - `repository`: `UserRepository` and `StressHistoryRepository` for database queries.
    - `dto`: API payload request/response mappings.
    - `client`: `MLClient` for communications with Python.
    - `service`: `UserService`, `PredictService`, `HistoryService`, and `ChatService`.
    - `controller`: Controllers mapping `/signup`, `/login`, `/profile`, `/predict`, `/history/{userId}`, and `/chat_api`.
    - `exception`: Custom exceptions and `GlobalExceptionHandler` returning clean JSON.

---

## 1. Cloud MongoDB Setup

1. Provision a MongoDB Cluster on MongoDB Atlas or another cloud provider.
2. In the `calmpulse` database, your collections are `users` and `stress_history`.
3. Configure the following environment variable on the computer running the Spring Boot backend:
   - `MONGO_URI`: The full connection string for your MongoDB cluster (e.g., `mongodb+srv://ajitbirajdar1108:Ajit%401108@cluster0.z6qsfui.mongodb.net/calmpulse?retryWrites=true&w=majority&appName=Cluster0`).
   - If not set, it defaults to the user's direct MongoDB URI in `application.properties`.

---

## 2. Running the Python ML Prediction Service

Make sure python dependencies (`pandas`, `numpy`, `scikit-learn`, `flask`) are installed, then run the service:

```bash
cd d:\Ajit\Miniproject\ML
python prediction_service.py
```
The ML microservice will load the models and run on `http://localhost:5001`.

---

## 3. Running the Spring Boot Backend

### Configuration
Update the Gemini API Key in [application.properties](file:///d:/Ajit/Miniproject/backend/src/main/resources/application.properties) or set the `GEMINI_API_KEY` environment variable:
```properties
gemini.api.key=YOUR_GEMINI_API_KEY
```

### Compile & Run
Execute the following commands in the `backend` folder:
```bash
cd d:\Ajit\Miniproject\backend
mvn clean compile
mvn spring-boot:run
```
The server will start on `http://localhost:8080`.
- Swagger UI will be available at: `http://localhost:8080/swagger-ui/index.html`
- OpenAPI Specification at: `http://localhost:8080/v3/api-docs`

---

## 4. Running the Frontend

Open [index.html](file:///d:/Ajit/Miniproject/Front%20end/CalmPulse/index.html) in your browser. All interactions (Sign In, Sign Up, Dashboard, History, Chatbot) will communicate through the Spring Boot API at `http://localhost:8080`, which stores data in MongoDB and delegates predictions to the Python microservice.

---

## Summary of Migrated Files

| Category | File Path | Status | Purpose |
| :--- | :--- | :--- | :--- |
| **Frontend Config** | [api-config.js](file:///d:/Ajit/Miniproject/Front%20end/CalmPulse/api-config.js) | Modified | Pointed API base URL to `http://localhost:8080` |
| **Python Service** | [prediction_service.py](file:///d:/Ajit/Miniproject/ML/prediction_service.py) | Created | Lightweight Python Flask ML prediction endpoint |
| **Spring Config** | [pom.xml](file:///d:/Ajit/Miniproject/backend/pom.xml) | Modified | Added Spring Data MongoDB and Lombok plugin |
| **Spring Config** | [application.properties](file:///d:/Ajit/Miniproject/backend/src/main/resources/application.properties) | Modified | Replaced MySQL configuration with MongoDB URI |
| **Spring Security** | [SecurityConfig.java](file:///d:/Ajit/Miniproject/backend/src/main/java/com/calmpulse/backend/config/SecurityConfig.java) | Created | Permit-all configurations & CORS settings |
| **Spring Config** | [AppConfig.java](file:///d:/Ajit/Miniproject/backend/src/main/java/com/calmpulse/backend/config/AppConfig.java) | Created | RestTemplate & BCrypt beans |
| **Mongo Documents** | [User.java](file:///d:/Ajit/Miniproject/backend/src/main/java/com/calmpulse/backend/entity/User.java) | Refactored | Maps users collection |
| **Mongo Documents** | [StressHistory.java](file:///d:/Ajit/Miniproject/backend/src/main/java/com/calmpulse/backend/entity/StressHistory.java) | Refactored | Maps stress history collection |
| **Mongo Repositories** | [UserRepository.java](file:///d:/Ajit/Miniproject/backend/src/main/java/com/calmpulse/backend/repository/UserRepository.java) | Refactored | MongoDB data operations for users |
| **Mongo Repositories** | [StressHistoryRepository.java](file:///d:/Ajit/Miniproject/backend/src/main/java/com/calmpulse/backend/repository/StressHistoryRepository.java) | Refactored | MongoDB data queries for history |
| **ML Client** | [MLClient.java](file:///d:/Ajit/Miniproject/backend/src/main/java/com/calmpulse/backend/client/MLClient.java) | Created | REST connection to Python Prediction service |
| **Services** | [UserService.java](file:///d:/Ajit/Miniproject/backend/src/main/java/com/calmpulse/backend/service/UserService.java) | Refactored | Auth and profiles business logic using String IDs |
| **Services** | [PredictService.java](file:///d:/Ajit/Miniproject/backend/src/main/java/com/calmpulse/backend/service/PredictService.java) | Refactored | Calls Python prediction, logs records to MongoDB |
| **Services** | [HistoryService.java](file:///d:/Ajit/Miniproject/backend/src/main/java/com/calmpulse/backend/service/HistoryService.java) | Refactored | Retrieves history from MongoDB collections |
| **Services** | [ChatService.java](file:///d:/Ajit/Miniproject/backend/src/main/java/com/calmpulse/backend/service/ChatService.java) | Created | Relays wellness prompts to Gemini |
| **Controllers** | [AuthController.java](file:///d:/Ajit/Miniproject/backend/src/main/java/com/calmpulse/backend/controller/AuthController.java) | Created | Auth endpoints (`/signup`, `/login`) |
| **Controllers** | [ProfileController.java](file:///d:/Ajit/Miniproject/backend/src/main/java/com/calmpulse/backend/controller/ProfileController.java) | Created | Profiles endpoint (`/profile`) |
| **Controllers** | [PredictController.java](file:///d:/Ajit/Miniproject/backend/src/main/java/com/calmpulse/backend/controller/PredictController.java) | Created | Predictions endpoint (`/predict`) |
| **Controllers** | [HistoryController.java](file:///d:/Ajit/Miniproject/backend/src/main/java/com/calmpulse/backend/controller/HistoryController.java) | Created | History logs endpoint (`/history/{userId}`) |
| **Controllers** | [ChatController.java](file:///d:/Ajit/Miniproject/backend/src/main/java/com/calmpulse/backend/controller/ChatController.java) | Created | Assistant endpoint (`/chat_api`) |
| **Exceptions** | [GlobalExceptionHandler.java](file:///d:/Ajit/Miniproject/backend/src/main/java/com/calmpulse/backend/exception/GlobalExceptionHandler.java) | Refactored | Handles validation, resource not found and general exceptions |
| **Exceptions** | [ResourceNotFoundException.java](file:///d:/Ajit/Miniproject/backend/src/main/java/com/calmpulse/backend/exception/ResourceNotFoundException.java) | Created | Generic resource not found exception |
| **Exceptions** | [DuplicateEmailException.java](file:///d:/Ajit/Miniproject/backend/src/main/java/com/calmpulse/backend/exception/DuplicateEmailException.java) | Created | Thrown on duplicate signup attempt |
| **Exceptions** | [InvalidCredentialsException.java](file:///d:/Ajit/Miniproject/backend/src/main/java/com/calmpulse/backend/exception/InvalidCredentialsException.java) | Created | Thrown on login mismatch |
