package com.calmpulse.backend.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class HistoryResponse {

    @JsonProperty("stress_score")
    private Double stressScore;

    private String timestamp;

    private Factors factors;

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class Factors {

        @JsonProperty("sleep_quality")
        private String sleepQuality;

        @JsonProperty("working_hours")
        private Integer workingHours;

        @JsonProperty("work_hours")
        private Integer workHours; // Duplicate for frontend compatibility

        @JsonProperty("virtual_meetings")
        private Integer virtualMeetings;

        @JsonProperty("anxiety_level")
        private Integer anxietyLevel;

        private Integer depression;
    }
}
