package com.calmpulse.backend.repository;

import com.calmpulse.backend.entity.StressHistory;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface StressHistoryRepository extends MongoRepository<StressHistory, String> {
    List<StressHistory> findByUserId(String userId);
}
