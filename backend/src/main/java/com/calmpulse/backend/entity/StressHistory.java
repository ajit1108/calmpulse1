package com.calmpulse.backend.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;
import lombok.*;
import java.time.LocalDateTime;

@Document(collection = "stress_history")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class StressHistory {

    @Id
    private String id;

    @Field("user_id")
    private String userId;

    @Field("stress_score")
    private Double stressScore;

    @Field("timestamp")
    private String timestamp; // Using String timestamp for MongoDB compatibility (matches isoformat string in app.py)

    @Field("job_role")
    private String jobRole;

    @Field("working_hours")
    private Integer workingHours;

    @Field("virtual_meetings")
    private Integer virtualMeetings;

    @Field("work_life_balance")
    private Integer workLifeBalance;

    @Field("access_to_mental_health")
    private String accessToMentalHealth;

    @Field("satisfaction_with_remote_work")
    private String satisfactionWithRemoteWork;

    @Field("company_support")
    private Integer companySupport;

    @Field("physical_activity")
    private String physicalActivity;

    @Field("sleep_quality")
    private String sleepQuality;

    @Field("anxiety_level")
    private Integer anxietyLevel;

    @Field("depression")
    private Integer depression;

    @Field("academic_performance")
    private Integer academicPerformance;

    @Field("study_load")
    private Integer studyLoad;

    @Field("teacher_student_relationship")
    private Integer teacherStudentRelationship;

    @Field("future_career_concerns")
    private Integer futureCareerConcerns;

    @Field("social_support")
    private Integer socialSupport;

    @Field("peer_pressure")
    private Integer peerPressure;

    @Field("extracurricular_load")
    private Integer extracurricularLoad;
}
