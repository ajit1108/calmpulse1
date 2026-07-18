package com.calmpulse.backend.service;

import com.calmpulse.backend.client.MLClient;
import com.calmpulse.backend.dto.PredictRequest;
import com.calmpulse.backend.dto.PredictResponse;
import com.calmpulse.backend.entity.StressHistory;
import com.calmpulse.backend.entity.User;
import com.calmpulse.backend.exception.ResourceNotFoundException;
import com.calmpulse.backend.repository.StressHistoryRepository;
import com.calmpulse.backend.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

@Service
public class PredictService {

    private final MLClient mlClient;
    private final UserRepository userRepository;
    private final StressHistoryRepository stressHistoryRepository;

    public PredictService(MLClient mlClient, UserRepository userRepository, StressHistoryRepository stressHistoryRepository) {
        this.mlClient = mlClient;
        this.userRepository = userRepository;
        this.stressHistoryRepository = stressHistoryRepository;
    }

    public PredictResponse predict(PredictRequest request) {
        String userId = request.getUserId();
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User not found with id: " + userId));

        // Call the Python microservice for ML prediction
        Double stressScore = mlClient.predictStressScore(user.getRole(), request);

        // Build and save history record to MongoDB
        StressHistory history = StressHistory.builder()
                .userId(userId)
                .stressScore(stressScore)
                .timestamp(LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME))
                .jobRole(request.getJobRole())
                .workingHours(request.getWorkingHours())
                .virtualMeetings(request.getVirtualMeetings())
                .workLifeBalance(request.getWorkLifeBalance())
                .accessToMentalHealth(request.getAccessToMentalHealth())
                .satisfactionWithRemoteWork(request.getSatisfactionWithRemoteWork())
                .companySupport(request.getCompanySupport())
                .physicalActivity(request.getPhysicalActivity())
                .sleepQuality(request.getSleepQuality())
                .anxietyLevel(request.getAnxietyLevel())
                .depression(request.getDepression())
                .academicPerformance(request.getAcademicPerformance())
                .studyLoad(request.getStudyLoad())
                .teacherStudentRelationship(request.getTeacherStudentRelationship())
                .futureCareerConcerns(request.getFutureCareerConcerns())
                .socialSupport(request.getSocialSupport())
                .peerPressure(request.getPeerPressure())
                .extracurricularLoad(request.getExtracurricularLoad())
                .build();

        stressHistoryRepository.save(history);

        // Generate suggestions based on user role and stress score
        List<String> suggestions = generateSuggestions(stressScore, user.getRole());

        return PredictResponse.builder()
                .stressScore(stressScore)
                .suggestions(suggestions)
                .build();
    }

    private List<String> generateSuggestions(Double stressScore, String role) {
        List<String> suggestions = new ArrayList<>();
        if ("employee".equalsIgnoreCase(role)) {
            // Employee stress levels: 1 (Low), 2 (Moderate), 3 (High)
            if (stressScore >= 2.5) {
                suggestions.add("High stress detected. Take rest and manage workload.");
            } else if (stressScore >= 1.5) {
                suggestions.add("Moderate stress detected. Improve work-life balance.");
            } else {
                suggestions.add("Low stress. Keep maintaining healthy habits.");
            }
        } else {
            // Student stress levels: 0 (Low), 1 (Moderate), 2 (High)
            if (stressScore >= 1.5) {
                suggestions.add("High stress detected. Talk with mentor or counselor.");
            } else if (stressScore >= 0.5) {
                suggestions.add("Moderate stress detected. Take regular breaks.");
            } else {
                suggestions.add("Low stress. Continue healthy study habits.");
            }
        }
        return suggestions;
    }
}
