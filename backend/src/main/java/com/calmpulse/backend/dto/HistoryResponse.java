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

        @JsonProperty("work_life_balance")
        private Integer workLifeBalance;

        @JsonProperty("access_to_mental_health")
        private String accessToMentalHealth;

        @JsonProperty("satisfaction_with_remote_work")
        private String satisfactionWithRemoteWork;

        @JsonProperty("company_support")
        private Integer companySupport;

        @JsonProperty("physical_activity")
        private String physicalActivity;

        @JsonProperty("academic_performance")
        private Integer academicPerformance;

        @JsonProperty("study_load")
        private Integer studyLoad;

        @JsonProperty("teacher_student_relationship")
        private Integer teacherStudentRelationship;

        @JsonProperty("future_career_concerns")
        private Integer futureCareerConcerns;

        @JsonProperty("social_support")
        private Integer socialSupport;

        @JsonProperty("peer_pressure")
        private Integer peerPressure;

        @JsonProperty("extracurricular_load")
        private Integer extracurricularLoad;
    }
}
