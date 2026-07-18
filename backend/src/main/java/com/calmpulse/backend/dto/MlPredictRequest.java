package com.calmpulse.backend.dto;

import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class MlPredictRequest {
    private String role;
    private Object data; // Can hold student or employee predict fields
}
