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

        try {
            ResponseEntity<MlPredictResponse> response = restTemplate.postForEntity(
                    endpoint,
                    requestEntity,
                    MlPredictResponse.class
            );

            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null && response.getBody().getStressScore() != null) {
                Double score = response.getBody().getStressScore();
                log.info("Successfully received stress score from ML service: {}", score);
                return score;
            } else {
                log.error("ML service returned unsuccessful response: {}", response.getStatusCode());
                throw new RuntimeException("ML service returned status: " + response.getStatusCode());
            }

        } catch (RestClientException e) {
            log.error("Error communicating with Python ML microservice: {}", e.getMessage());
            throw new RuntimeException("Unable to contact ML microservice. Details: " + e.getMessage(), e);
        }
    }
}
