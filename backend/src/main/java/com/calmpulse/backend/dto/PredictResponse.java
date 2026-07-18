package com.calmpulse.backend.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.*;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class PredictResponse {

    @JsonProperty("stress_score")
    private Double stressScore;

    private List<String> suggestions;
}
