package com.calmpulse.backend.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class MlPredictResponse {
    @JsonProperty("stress_score")
    private Double stressScore;
}
