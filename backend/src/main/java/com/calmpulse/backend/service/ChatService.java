package com.calmpulse.backend.service;

import com.calmpulse.backend.dto.ChatRequest;
import com.calmpulse.backend.dto.ChatResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.Map;

@Service
public class ChatService {

    private static final Logger log = LoggerFactory.getLogger(ChatService.class);

    private final RestTemplate restTemplate;
    private final String geminiApiUrl;
    private final String geminiApiKey;

    public ChatService(RestTemplate restTemplate,
                       @Value("${gemini.api.url}") String geminiApiUrl,
                       @Value("${gemini.api.key}") String geminiApiKey) {
        this.restTemplate = restTemplate;
        this.geminiApiUrl = geminiApiUrl;
        this.geminiApiKey = geminiApiKey;
    }

    @SuppressWarnings("rawtypes")
    public ChatResponse chat(ChatRequest request) {
        String prompt = "You are a calm mental wellness assistant.\n" +
                "User role: " + request.getUserRole() + "\n\n" +
                "User message:\n" +
                request.getMessage();

        log.info("Contacting Gemini API with user message...");

        // Build the request body for Gemini AI API
        Map<String, Object> part = Map.of("text", prompt);
        Map<String, Object> content = Map.of("parts", List.of(part));
        Map<String, Object> requestPayload = Map.of("contents", List.of(content));

        // Format request URL with API Key
        String urlWithKey = geminiApiUrl + "?key=" + geminiApiKey;

        try {
            Map responseMap = restTemplate.postForObject(urlWithKey, requestPayload, Map.class);
            if (responseMap == null) {
                return ChatResponse.builder().response("AI service unavailable").build();
            }

            // Parse response: responseMap.candidates[0].content.parts[0].text
            List candidates = (List) responseMap.get("candidates");
            if (candidates != null && !candidates.isEmpty()) {
                Map candidate = (Map) candidates.get(0);
                Map contentMap = (Map) candidate.get("content");
                if (contentMap != null) {
                    List parts = (List) contentMap.get("parts");
                    if (parts != null && !parts.isEmpty()) {
                        Map partMap = (Map) parts.get(0);
                        String text = (String) partMap.get("text");
                        return ChatResponse.builder().response(text).build();
                    }
                }
            }

            log.warn("Gemini API returned an unexpected response structure: {}", responseMap);
            return ChatResponse.builder().response("Sorry, I couldn't get a proper response.").build();

        } catch (Exception e) {
            log.error("Error communicating with Gemini API: {}", e.getMessage(), e);
            return ChatResponse.builder().response("AI service error: " + e.getMessage()).build();
        }
    }
}
