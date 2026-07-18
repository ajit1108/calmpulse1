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
                    .build();

            return HistoryResponse.builder()
                    .stressScore(record.getStressScore())
                    .timestamp(record.getTimestamp() != null ? record.getTimestamp() : "")
                    .factors(factors)
                    .build();
        }).collect(Collectors.toList());
    }
}
