package com.example.verificationservice.service;

import com.example.verificationservice.model.CustomerData;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.io.InputStream;
import java.util.Random;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Service
public class VerificationService {

    private final Random random = new Random();
    private final ObjectMapper objectMapper = new ObjectMapper();

    // API 1 Logic: Parse Bank Statement (JSON or PDF)
    public CustomerData parseBankStatement(MultipartFile file) throws IOException {
        String contentType = file.getContentType();
        if (contentType != null && contentType.equals("application/json")) {
            return objectMapper.readValue(file.getInputStream(), CustomerData.class);
        } else if (contentType != null && contentType.equals("application/pdf")) {
            return parsePdf(file.getInputStream());
        } else {
            throw new IllegalArgumentException("Unsupported file type: " + contentType);
        }
    }

    private CustomerData parsePdf(InputStream pdfStream) throws IOException {
        try (PDDocument document = PDDocument.load(pdfStream)) {
            PDFTextStripper stripper = new PDFTextStripper();
            String text = stripper.getText(document);

            // Simple regex to find name and address (this would be more complex in reality)
            String firstName = findValue(text, "First Name: (\\w+)");
            String lastName = findValue(text, "Last Name: (\\w+)");
            String address = findValue(text, "Address: (.+)");

            return new CustomerData(firstName, lastName, address);
        }
    }

    private String findValue(String text, String regex) {
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(text);
        return matcher.find() ? matcher.group(1).trim() : "Not Found";
    }
 public CustomerData getMockBankStatement(String firstName, String lastName, String address) {
        double chance = random.nextDouble();

        if (chance < 0.8) { // 80% chance of perfect match
            return new CustomerData(firstName, lastName, address);
        } else if (chance < 0.9) { // 10% chance of partial mismatch
            return new CustomerData(firstName, "Doh", "1".concat(address)); // Typo + "Street"
        } else { // 10% chance of complete failure
            return new CustomerData("Jane", "Smith",address);
        }
    }

    // API 2 Logic: Mock Credit Report with Data Variation
    public CustomerData getMockCreditReport(String firstName, String lastName, String ssn) {
        double chance = random.nextDouble();

        if (chance < 0.8) { // 80% chance of perfect match
            return new CustomerData(firstName, lastName, "123 Main St, Anytown, USA");
        } else if (chance < 0.9) { // 10% chance of partial mismatch
            return new CustomerData(firstName, "Doh", "123 Main Street, Anytown, USA"); // Typo + "Street"
        } else { // 10% chance of complete failure
            return new CustomerData("Jane", "Smith", "456 Other Ave, Elsewhere, USA");
        }
    }
}