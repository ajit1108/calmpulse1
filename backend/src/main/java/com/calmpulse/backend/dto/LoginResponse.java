package com.calmpulse.backend.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class LoginResponse {

    private String message;

    @JsonProperty("user_id")
    private String userId;

    @JsonProperty("is_new_user")
    private Boolean isNewUser;

    private String role;
}
