package com.calmpulse.backend.controller;

import com.calmpulse.backend.dto.HistoryResponse;
import com.calmpulse.backend.service.HistoryService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/history")
@Tag(name = "Prediction History", description = "Endpoints for fetching previous stress test runs")
public class HistoryController {

    private final HistoryService historyService;

    public HistoryController(HistoryService historyService) {
        this.historyService = historyService;
    }

    @GetMapping("/{userId}")
    @Operation(summary = "Retrieve stress test history", description = "Fetches list of all previous stress test scores and factor breakdowns for a user")
    public ResponseEntity<List<HistoryResponse>> getHistory(@PathVariable String userId) {
        List<HistoryResponse> history = historyService.getHistory(userId);
        return ResponseEntity.ok(history);
    }
}
