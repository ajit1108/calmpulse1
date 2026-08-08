package com.calmpulse.backend.service;

import com.calmpulse.backend.dto.HistoryResponse;
import com.calmpulse.backend.entity.StressHistory;
import com.calmpulse.backend.repository.StressHistoryRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class HistoryService {

    private final StressHistoryRepository stressHistoryRepository;

    public HistoryService(StressHistoryRepository stressHistoryRepository) {
        this.stressHistoryRepository = stressHistoryRepository;
    }

    public List<HistoryResponse> getHistory(String userId) {
        List<StressHistory> records = stressHistoryRepository.findByUserId(userId);

        return records.stream().map(record -> {
            HistoryResponse.Factors factors = HistoryResponse.Factors.builder()
                    .sleepQuality(record.getSleepQuality())
                    .workingHours(record.getWorkingHours())
                    .workHours(record.getWorkingHours()) // Duplicate for frontend compatibility
                    .virtualMeetings(record.getVirtualMeetings())
                    .anxietyLevel(record.getAnxietyLevel())
                    .depression(record.getDepression())
                    .workLifeBalance(record.getWorkLifeBalance())
                    .accessToMentalHealth(record.getAccessToMentalHealth())
                    .satisfactionWithRemoteWork(record.getSatisfactionWithRemoteWork())
                    .companySupport(record.getCompanySupport())
                    .physicalActivity(record.getPhysicalActivity())
                    .academicPerformance(record.getAcademicPerformance())
                    .studyLoad(record.getStudyLoad())
                    .teacherStudentRelationship(record.getTeacherStudentRelationship())
                    .futureCareerConcerns(record.getFutureCareerConcerns())
                    .socialSupport(record.getSocialSupport())
                    .peerPressure(record.getPeerPressure())
                    .extracurricularLoad(record.getExtracurricularLoad())
                    .build();

            String ts = record.getTimestamp();
            if (ts == null || ts.isEmpty()) {
                ts = record.getCreatedAt();
            }
            if (ts == null || ts.isEmpty()) {
                ts = record.getDate();
            }
            if (ts == null) {
                ts = "";
            }
            if (!ts.isEmpty() && !ts.endsWith("Z") && !ts.contains("+") && ts.indexOf('T') > 0) {
                ts = ts + "Z";
            }

            Double sScore = record.getStressScore();
            if (sScore == null) {
                sScore = record.getPrediction();
            }
            if (sScore == null) {
                sScore = record.getScore();
            }
            if (sScore == null) {
                sScore = 0.0;
            }

            return HistoryResponse.builder()
                    .stressScore(sScore)
                    .prediction(record.getPrediction())
                    .predictionType(record.getPredictionType())
                    .createdAt(record.getCreatedAt())
                    .date(record.getDate())
                    .score(record.getScore())
                    .mood(record.getMood())
                    .stress(record.getStress())
                    .anxiety(record.getAnxiety())
                    .timestamp(ts)
                    .factors(factors)
                    .build();
        }).collect(Collectors.toList());
    }
}
