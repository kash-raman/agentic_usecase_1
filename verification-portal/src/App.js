import React, { useState } from 'react';

// --- Basic Styling for the Component ---
const styles = {
  container: {
    fontFamily: 'Arial, sans-serif',
    maxWidth: '700px',
    margin: '40px auto',
    padding: '30px',
    border: '1px solid #ddd',
    borderRadius: '8px',
    boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
    backgroundColor: '#f9f9f9',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
  },
  formGroup: {
    display: 'flex',
    flexDirection: 'column',
  },
  label: {
    marginBottom: '8px',
    fontWeight: 'bold',
    color: '#333',
  },
  input: {
    padding: '10px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    fontSize: '16px',
  },
  button: {
    padding: '12px 20px',
    border: 'none',
    borderRadius: '4px',
    backgroundColor: '#007bff',
    color: 'white',
    fontSize: '16px',
    cursor: 'pointer',
    marginTop: '10px',
  },
  radioGroup: {
    display: 'flex',
    gap: '20px',
    alignItems: 'center',
    marginBottom: '10px',
  },
  textArea: {
    padding: '10px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    fontSize: '14px',
    minHeight: '120px',
    fontFamily: 'monospace',
  },
  submittedData: {
    marginTop: '30px',
    padding: '20px',
    backgroundColor: '#e9ecef',
    border: '1px solid #ced4da',
    borderRadius: '4px',
  },
  pre: {
    whiteSpace: 'pre-wrap',
    wordWrap: 'break-word',
    backgroundColor: '#fff',
    padding: '15px',
    borderRadius: '4px',
  },
  h1: {
    textAlign: 'center',
    color: '#2c3e50',
  },
  h3: {
    color: '#34495e',
    borderBottom: '2px solid #007bff',
    paddingBottom: '5px',
  }
};

// --- Placeholder JSON to guide the user ---
const placeholderJson = JSON.stringify(
  {
    name: "John Doe",
    address: "123 Main St, Anytown, USA 12345",
  },
  null,
  2
);


function App() {
  // State for user details
  const [name, setName] = useState('');
  const [address, setAddress] = useState('');
  const [ssn, setSsn] = useState('');

  // State to toggle between 'upload' and 'json' input types
  const [inputType, setInputType] = useState('upload');

  // State for file uploads
  const [creditReportFile, setCreditReportFile] = useState(null);
  const [bankStatementFile, setBankStatementFile] = useState(null);

  // State for JSON text inputs
  const [creditReportJson, setCreditReportJson] = useState(placeholderJson);
  const [bankStatementJson, setBankStatementJson] = useState(placeholderJson);

  // State to display the final collected data
  const [submittedData, setSubmittedData] = useState(null);

  const handleSubmit = (event) => {
    event.preventDefault(); // Prevent page reload

    const formData = {
      userDetails: { name, address, ssn },
      documentDetails: {},
    };

    if (inputType === 'upload') {
      formData.documentDetails = {
        inputType: 'File Upload',
        creditReport: creditReportFile ? { name: creditReportFile.name, size: creditReportFile.size } : 'Not Provided',
        bankStatement: bankStatementFile ? { name: bankStatementFile.name, size: bankStatementFile.size } : 'Not Provided',
      };
    } else { // inputType is 'json'
      try {
        formData.documentDetails = {
          inputType: 'JSON Input',
          creditReport: JSON.parse(creditReportJson),
          bankStatement: JSON.parse(bankStatementJson),
        };
      } catch (error) {
        alert('Invalid JSON provided. Please check the format and try again.');
        return; // Stop the submission
      }
    }
    setSubmittedData(formData);
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.h1}>Document Verification Portal</h1>
      <form onSubmit={handleSubmit} style={styles.form}>
        <div style={styles.formGroup}>
          <label style={styles.label}>Full Name</label>
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} style={styles.input} required />
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label}>Full Address</label>
          <input type="text" value={address} onChange={(e) => setAddress(e.target.value)} style={styles.input} required />
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label}>Social Security Number (SSN)</label>
          <input type="password" value={ssn} onChange={(e) => setSsn(e.target.value)} style={styles.input} required />
        </div>

        <h3 style={styles.h3}>Provide Documents</h3>
        <div style={styles.radioGroup}>
          <label>
            <input type="radio" value="upload" checked={inputType === 'upload'} onChange={(e) => setInputType(e.target.value)} />
            File Upload
          </label>
          <label>
            <input type="radio" value="json" checked={inputType === 'json'} onChange={(e) => setInputType(e.target.value)} />
            JSON Input
          </label>
        </div>

        {/* --- Conditional Rendering Section --- */}
        {inputType === 'upload' ? (
          <>
            <div style={styles.formGroup}>
              <label style={styles.label}>Credit Report Document</label>
              <input type="file" onChange={(e) => setCreditReportFile(e.target.files[0])} style={styles.input} />
            </div>
            <div style={styles.formGroup}>
              <label style={styles.label}>Bank Statement Document</label>
              <input type="file" onChange={(e) => setBankStatementFile(e.target.files[0])} style={styles.input} />
            </div>
          </>
        ) : (
          <>
            <div style={styles.formGroup}>
              <label style={styles.label}>Credit Report (JSON)</label>
              <textarea value={creditReportJson} onChange={(e) => setCreditReportJson(e.target.value)} style={styles.textArea}></textarea>
            </div>
            <div style={styles.formGroup}>
              <label style={styles.label}>Bank Statement (JSON)</label>
              <textarea value={bankStatementJson} onChange={(e) => setBankStatementJson(e.target.value)} style={styles.textArea}></textarea>
            </div>
          </>
        )}

        <button type="submit" style={styles.button}>Submit Verification</button>
      </form>

      {/* --- Display Submitted Data --- */}
      {submittedData && (
        <div style={styles.submittedData}>
          <h3 style={styles.h3}>Submission Captured</h3>
          <p>The following data has been collected and would be sent to the verification service:</p>
          <pre style={styles.pre}>
            <code>{JSON.stringify(submittedData, null, 2)}</code>
          </pre>
        </div>
      )}
    </div>
  );
}

export default App;