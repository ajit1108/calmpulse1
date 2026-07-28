package com.calmpulse.backend.controller;

import com.calmpulse.backend.entity.User;
import com.calmpulse.backend.service.UserService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
@RequestMapping("/user")
@Tag(name = "User Stats", description = "Endpoints for retrieving user streak and details")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/{userId}/info")
    @Operation(summary = "Get user streak and badge info", description = "Retrieves user's login streak and earned badges")
    public ResponseEntity<Map<String, Object>> getUserInfo(@PathVariable String userId) {
        User user = userService.getUserById(userId);
        return ResponseEntity.ok(Map.of(
            "streak", user.getStreak() != null ? user.getStreak() : 0,
            "longestStreak", user.getLongestStreak() != null ? user.getLongestStreak() : 0,
            "badge", user.getBadge() != null ? user.getBadge() : "None"
        ));
    }
}
