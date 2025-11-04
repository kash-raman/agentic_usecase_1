package com.example.verificationservice.controller;

import com.example.verificationservice.model.CustomerData;
import com.example.verificationservice.service.VerificationService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

@RestController
public class VerificationController {

    private final VerificationService verificationService;

    public VerificationController(VerificationService verificationService) {
        this.verificationService = verificationService;
    }

    @PostMapping("/verify/bank-statement")
    public ResponseEntity<CustomerData> verifyBankAccount(@RequestParam("file") MultipartFile file) {
        try {
            CustomerData data = verificationService.parseBankStatement(file);
            return ResponseEntity.ok(data);
        } catch (IOException | IllegalArgumentException e) {
            return ResponseEntity.badRequest().build();
        }
    }
 @PostMapping("/bank-statement")
    public ResponseEntity<CustomerData> verifyBankAccount( @RequestParam String firstName,
            @RequestParam String lastName, @RequestParam String address ) {
      
            CustomerData data = verificationService.getMockBankStatement(firstName, lastName, address);
            return ResponseEntity.ok(data);
       
    }
    @GetMapping("/credit-report")
    public ResponseEntity<CustomerData> getCreditReport(
            @RequestParam String firstName,
            @RequestParam String lastName,
            @RequestParam String ssn) {
        CustomerData data = verificationService.getMockCreditReport(firstName, lastName, ssn);
        return ResponseEntity.ok(data);
    }
}