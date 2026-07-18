package com.calmpulse.backend.controller;

import com.calmpulse.backend.dto.PredictRequest;
import com.calmpulse.backend.dto.PredictResponse;
import com.calmpulse.backend.service.PredictService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/predict")
@Tag(name = "Stress Prediction", description = "Endpoints for running ML predictions and recommendations")
public class PredictController {

    private final PredictService predictService;

    public PredictController(PredictService predictService) {
        this.predictService = predictService;
    }

    @PostMapping
    @Operation(summary = "Calculate stress score", description = "Forwards metrics to Python service, logs entry to Cloud MySQL database, and returns suggestions")
    public ResponseEntity<PredictResponse> predict(@RequestBody PredictRequest request) {
        PredictResponse response = predictService.predict(request);
        return ResponseEntity.ok(response);
    }
}
