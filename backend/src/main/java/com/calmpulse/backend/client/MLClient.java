package com.calmpulse.backend.client;

import com.calmpulse.backend.dto.MlPredictRequest;
import com.calmpulse.backend.dto.MlPredictResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

@Component
public class MLClient {

    private static final Logger log = LoggerFactory.getLogger(MLClient.class);

    private final RestTemplate restTemplate;
    private final String mlServiceUrl;

    public MLClient(RestTemplate restTemplate, @Value("${ml.service.url}") String mlServiceUrl) {
        this.restTemplate = restTemplate;
        this.mlServiceUrl = mlServiceUrl;
    }

    public Double predictStressScore(String role, Object data) {
        String endpoint = mlServiceUrl + "/predict_ml";
        log.info("Sending prediction request to Python ML Service at: {}", endpoint);

        MlPredictRequest requestPayload = MlPredictRequest.builder()
                .role(role)
                .data(data)
                .build();

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<MlPredictRequest> requestEntity = new HttpEntity<>(requestPayload, headers);

        int maxRetries = 3;
        int delayMs = 3000;
        ResponseEntity<MlPredictResponse> response = null;
        Exception lastException = null;

        for (int i = 0; i < maxRetries; i++) {
            try {
                log.info("Sending prediction request to Python ML Service (Attempt {}/{})", i + 1, maxRetries);
                response = restTemplate.postForEntity(
                        endpoint,
                        requestEntity,
                        MlPredictResponse.class
                );
                if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                    break;
                }
            } catch (Exception e) {
                lastException = e;
                log.warn("Attempt {} failed to contact ML service: {}. Retrying in {}ms...", i + 1, e.getMessage(), delayMs);
                try {
                    Thread.sleep(delayMs);
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                    throw new RuntimeException("Prediction interrupted", ie);
                }
            }
        }

        if (response == null || !response.getStatusCode().is2xxSuccessful() || response.getBody() == null) {
            String errorMsg = lastException != null ? lastException.getMessage() : "Invalid response";
            log.error("Failed to contact Python ML service after {} attempts: {}", maxRetries, errorMsg);
            throw new RuntimeException("Unable to contact ML microservice. Details: " + errorMsg, lastException);
        }

        Double score = response.getBody().getStressScore();
        log.info("Successfully received stress score from ML service: {}", score);
        return score;
    }
}
