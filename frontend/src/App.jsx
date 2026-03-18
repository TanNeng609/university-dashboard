import { useState, useEffect } from 'react'
import './App.css'

function App() {
  // 1. STATE: This is React's memory. We create an empty list to hold the students.
  const [students, setStudents] = useState([]);

  const[name,setName]=useState("");
  const[course,setCourse]=useState("");
  const[gpa,setGpa]=useState("");

  // 2. EFFECT: This tells React to run this code the moment the page loads.
  useEffect(() => {
    console.log("Fetching data from Python Backend...");
    
    // We ping the Python server we built earlier!
    fetch('http://127.0.0.1:5000/api/students')
      .then(response => response.json()) // Turn the raw network data into JSON
      .then(data => {
        console.log("Data received:", data);
        setStudents(data); // Save the data into React's memory
      })
      .catch(error => console.error("Connection Failed:", error));
  }, []);

  const handleSubmit=(e)=>{
    e.preventDefault();

    const newStudentData={name:name,course:course,gpa:parseFloat(gpa)};

    fetch('http://127.0.0.1:5000/api/students',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify(newStudentData)
    })
    .then(response=>response.json())
    .then(data=>{
      console.log(data.message);

      setStudents([...students,data.student]);

      setName("");
      setCourse("");
      setGpa("");
    })
    .catch(error=>console.error("Failed to send data:",error))
  }

  // 3. UI: This is the HTML that React paints onto the screen.
  return (
    <div>
      <h1>🎓 University Dashboard</h1>
      <p>Live Data Stream from Python API Server</p>

      <div style={{backgroundColor:'#1a1a2e',padding:"20px",borderRadius:'10px',marginBottom:'30px'}}>
        <h3>Enroll New Student </h3>

        <form onSubmit={handleSubmit}style={{display:'flex',gap:'10px',justifyContent:'center'}}>
          <input type='text' placeholder='Student Name' value={name} onChange={(e)=>setName(e.target.value)}required/>
          <input type='text' placeholder='Major' value={course} onChange={(e)=>setCourse(e.target.value)}required/>
          <input type='number' step={0.1} placeholder='GPA' value={gpa} onChange={(e)=>setGpa(e.target.value)}required/>

          <button type='submit' style={{backgroundColor:'#4CAF50',color:'white',fontWeight:'bold'}}>
            submit
          </button>
        </form>
      </div>

      {/* We loop through the 'students' list and build a card for each one */}
      <div style={{ display: 'flex', gap: '20px', justifyContent: 'center', marginTop: '30px' }}>
        {students.map((student) => (
          <div key={student.id} style={{ border: '2px solid #646cff', padding: '20px', borderRadius: '10px' }}>
            <h2>{student.name}</h2>
            <p><strong>Major:</strong> {student.course}</p>
            <p><strong>GPA:</strong> {student.gpa}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App