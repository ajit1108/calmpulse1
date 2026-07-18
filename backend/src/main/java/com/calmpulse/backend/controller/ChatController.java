package com.calmpulse.backend.controller;

import com.calmpulse.backend.dto.ChatRequest;
import com.calmpulse.backend.dto.ChatResponse;
import com.calmpulse.backend.service.ChatService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/chat_api")
@Tag(name = "Wellness Chatbot", description = "Endpoints for mental health conversational assistant (Gemini)")
public class ChatController {

    private final ChatService chatService;

    public ChatController(ChatService chatService) {
        this.chatService = chatService;
    }

    @PostMapping
    @Operation(summary = "Ask the wellness chatbot", description = "Forwards message context to Gemini AI and returns an encouraging, calming response")
    public ResponseEntity<ChatResponse> chat(@Valid @RequestBody ChatRequest request) {
        ChatResponse response = chatService.chat(request);
        return ResponseEntity.ok(response);
    }
}
