package com.calmpulse.backend.controller;

import com.calmpulse.backend.dto.ProfileRequest;
import com.calmpulse.backend.service.UserService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
@RequestMapping("/profile")
@Tag(name = "User Profile", description = "Endpoints for updating user profile metrics")
public class ProfileController {

    private final UserService userService;

    public ProfileController(UserService userService) {
        this.userService = userService;
    }

    @PostMapping
    @Operation(summary = "Update user profile details", description = "Saves user profile attributes like age, gender, contact and role mode")
    public ResponseEntity<Map<String, String>> saveProfile(@RequestBody ProfileRequest request) {
        userService.saveProfile(request);
        return ResponseEntity.ok(Map.of("message", "Profile updated successfully"));
    }
}
