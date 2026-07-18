package com.calmpulse.backend.service;

import com.calmpulse.backend.dto.LoginRequest;
import com.calmpulse.backend.dto.LoginResponse;
import com.calmpulse.backend.dto.ProfileRequest;
import com.calmpulse.backend.dto.SignupRequest;
import com.calmpulse.backend.entity.User;
import com.calmpulse.backend.exception.DuplicateEmailException;
import com.calmpulse.backend.exception.InvalidCredentialsException;
import com.calmpulse.backend.exception.ResourceNotFoundException;
import com.calmpulse.backend.repository.UserRepository;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class UserService {

    private final UserRepository userRepository;
    private final BCryptPasswordEncoder passwordEncoder;

    public UserService(UserRepository userRepository, BCryptPasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public LoginResponse signup(SignupRequest request) {
        if (userRepository.findByEmail(request.getEmail()).isPresent()) {
            throw new DuplicateEmailException("Email already exists");
        }

        String hashedPassword = passwordEncoder.encode(request.getPassword());

        User user = User.builder()
                .email(request.getEmail())
                .passwordHash(hashedPassword)
                .firstName(request.getFirstName())
                .lastName(request.getLastName())
                .contact(request.getContact())
                .role(request.getRole() != null ? request.getRole() : "student") // Default role as student
                .isNewUser(true)
                .build();

        User savedUser = userRepository.save(user);

        return LoginResponse.builder()
                .message("User created successfully")
                .userId(savedUser.getId())
                .isNewUser(savedUser.getIsNewUser())
                .role(savedUser.getRole())
                .build();
    }

    public LoginResponse login(LoginRequest request) {
        User user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new InvalidCredentialsException("Invalid credentials"));

        if (!passwordEncoder.matches(request.getPassword(), user.getPasswordHash())) {
            throw new InvalidCredentialsException("Invalid credentials");
        }

        return LoginResponse.builder()
                .message("Login successful")
                .userId(user.getId())
                .isNewUser(user.getIsNewUser())
                .role(user.getRole())
                .build();
    }

    public void saveProfile(ProfileRequest request) {
        String id = request.getUserId();
        User user = userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("User not found with id: " + id));

        user.setFirstName(request.getFirstName());
        user.setLastName(request.getLastName());
        user.setAge(request.getAge());
        user.setGender(request.getGender());
        user.setContact(request.getContact());
        if (request.getMode() != null) {
            user.setRole(request.getMode());
        }
        user.setIsNewUser(false);

        userRepository.save(user);
    }
}
