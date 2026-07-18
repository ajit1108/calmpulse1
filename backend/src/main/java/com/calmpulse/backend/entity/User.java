package com.calmpulse.backend.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;
import lombok.*;

@Document(collection = "users")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class User {

    @Id
    private String id;

    @Field("first_name")
    private String firstName;

    @Field("last_name")
    private String lastName;

    @Field("contact")
    private String contact;

    @Field("email")
    private String email;

    @Field("password_hash")
    private String passwordHash;

    @Field("age")
    private Integer age;

    @Field("gender")
    private String gender;

    @Field("role")
    private String role;

    @Field("is_new_user")
    @Builder.Default
    private Boolean isNewUser = true;
}
