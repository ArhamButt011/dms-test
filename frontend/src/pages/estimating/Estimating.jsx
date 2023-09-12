import React, { useState, useEffect } from "react";
import "./Estimating.css";
import { Link } from "react-router-dom";
import axios from "axios";

const Estimator = () => {
  const [data, setData] = useState([]);
  const [filter, setFilter] = useState("");
  const [showModal, setShowModal] = useState(false); // State to control modal visibility
  const [dueDate, setDueDate] = useState("");
  const [projectName, setProjectName] = useState("");
  const [estimatorName, setEstimatorName] = useState("");
  const [Eststatus, setEstStatus] = useState("");
  const [location, setLocation] = useState("");
  const [bidAmount, setBidAmount] = useState("");
  const [bidder, setBidder] = useState("");
  const [companyName, setCompanyName] = useState("");

  useEffect(() => {
    // Fetch data from the API
    axios.get("http://127.0.0.1:8000/api/estimating/estimating/")
      .then((response) => response.data)
      .then((data) => {
        setData(data);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);

  const filteredData = data.filter(
    (customer) =>
      customer.Prjct_Name.toUpperCase().includes(filter.toUpperCase()) ||
      customer.status.toUpperCase().includes(filter.toUpperCase()) ||
      customer.due_date.toUpperCase().includes(filter.toUpperCase())
  );

  // Define a function to handle modal close
  const closeModal = () => {
    setShowModal(false);
    // Remove the 'modal-active' class when the modal is closed
    document.body.classList.remove("modal-active");
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const dataToPost = {
      Prjct_Name: projectName,
      due_date: dueDate,
      status: Eststatus,
      location: location,
      bid_amount: bidAmount,
      bidder: bidder,
      estimator: estimatorName,
      company: companyName,
    };
    axios.post("http://127.0.0.1:8000/api/estimating/estimating/", dataToPost)
      .then((response) => {
        console.log("Data posted successfully");
        console.log(response.data);
        setShowModal(false);
      })
      .catch((error) => {
        console.error("Error posting data:", error);
      });
  };

  const handleDueDateChange = (e) => {
    setDueDate(e.target.value);
  };

  const handleProjectNameChange = (e) => {
    setProjectName(e.target.value);
  };

  const handleEstimatorNameChange = (e) => {
    setEstimatorName(e.target.value);
  };

  const handleStatusChange = (e) => {
    setEstStatus(e.target.value);
  };

  const handleLocationChange = (e) => {
    setLocation(e.target.value);
  };

  const handleBidAmountChange = (e) => {
    setBidAmount(e.target.value);
  };

  const handleBidderChange = (e) => {
    setBidder(e.target.value);
  };
  const handleCompanyNameChange = (e) => {
    setCompanyName(e.target.value);
  };

  return (
    <>
      <div className={`estimator px-5 ${showModal ? "modal-active" : ""}`}>
        <h3>Estimating Summary</h3>
        <div className="inputbtn d-flex gap-2 px-5">
          <input
            type="text"
            placeholder="Filter by Project Name"
            value={filter}
            className="myinput p-2 rounded"
            onChange={(e) => setFilter(e.target.value)}
          />
          <button
            className="btn btn-success"
            onClick={() => setShowModal(true)}
          >
            New
          </button>
        </div>
        <div className="table-responsive pt-3">
          <table className="table table-striped  table-bordered table-hover text-center">
            <thead>
              <tr>
                <th>ID</th>
                {/* <th>Company</th> */}
                <th>Due Date</th>
                <th>Project Name</th>
                <th>Status</th>
                <th>Estimator</th>
                <th>Bidder</th>
                <th>Bid Amount</th>
                {/* <th>Location</th>
            <th>Start_Date</th>
            <th>Status</th> */}
              </tr>
            </thead>
            <tbody className="cursor-pointer">
              {filteredData.map((item) => (
                <tr key={item.id}>
                  <td>{item.id}</td>
                  <td>{item.due_date}</td>
                  {/* <td>{item.Company}</td> */}
                  <td>{item.Prjct_Name}</td>
                  <td>{item.status}</td>
                  <td>{item.estimator}</td>
                  <td>{item.bidder}</td>
                  <td>{item.bid_amount}</td>
                  {/* <td>{item.location}</td>
              <td>{item.start_date}</td>*/}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      {/* Modal Code */}
      {showModal && (
        <div className={`modal-container pt-5 ps-2 ${showModal ? "show" : ""}`}>
          <h4 className="text-center addnewtxt">Add New Estimating Entry</h4>
          <button className="close-btn" onClick={closeModal}></button>
          <div className="modal-content px-5">
            <form onSubmit={handleSubmit} className="d-flex flex-column">
              <div className="mb-3">
                <label htmlFor="dueDate" className="form-label">
                  Due_Date:
                </label>
                <input
                  type="date"
                  className="form-control"
                  id="dueDate"
                  value={dueDate}
                  onChange={handleDueDateChange}
                />
              </div>
              <div className="mb-3">
                <label htmlFor="projectName" className="form-label">
                  Project_Name:
                </label>
                <input
                  type="text"
                  className="form-control"
                  id="projectName"
                  value={projectName}
                  onChange={handleProjectNameChange}
                />
              </div>
              <div className="mb-3">
                <label htmlFor="companyName" className="form-label">
                  Company_Name:
                </label>
                <select
                  className="form-select"
                  id="companyName"
                  value={companyName}
                  onChange={handleCompanyNameChange}
                >
                  <option value="Select Company">Select Company</option>
                  <option value="Innovative Technology Solutions">Innovative Technology Solutions</option>
                  <option value="Programmers Force">Programmers Force</option>
                  <option value="PureLogics">PureLogics</option>
                </select>
              </div>
              
              {/* ****************************** */}

              
              <div className="mb-3">
                <label htmlFor="estimatorName" className="form-label">
                  Estimator_Name:
                </label>
                <select
                  className="form-select"
                  id="estimatorName"
                  value={estimatorName}
                  onChange={handleEstimatorNameChange}
                >
                  <option value=" ">Select_Estimator_Name</option>
                  <option value="Ali">Ali</option>
                  <option value="Naveed">Naveed</option>
                  <option value="Mubeen">Mubeen</option>
                </select>
              </div>
              <div className="mb-3">
                <label htmlFor="status" className="form-label">
                  Status:
                </label>
                <select
                  className="form-select"
                  id="status"
                  value={Eststatus}
                  onChange={handleStatusChange}
                >
                  <option value=" ">Select_Status</option>
                  <option value="onHold">OnHold</option>
                  <option value="working">Working</option>
                  <option value="complete">Complete</option>
                </select>
              </div>
              <div className="mb-3">
                <label htmlFor="location" className="form-label">
                  Location:
                </label>
                <select
                  className="form-select"
                  id="location"
                  value={location}
                  onChange={handleLocationChange}
                >
                  <option value=" ">Select-Location</option>
                  <option value="SA">SA</option>
                  <option value="VA">VA</option>
                  <option value="NV">NV</option>
                  <option value="SF">SF</option>
                  <option value="STN">STN</option>
                  <option value="PHL">PHL</option>
                  <option value="FL">FL</option>
                </select>
              </div>
              <div className="mb-3">
                <label htmlFor="bidAmount" className="form-label">
                  Bid-Amount:
                </label>
                <input
                  type="number"
                  className="form-control"
                  id="bidAmount"
                  value={bidAmount}
                  onChange={handleBidAmountChange}
                />
              </div>
              <div className="mb-3">
                <label htmlFor="bidder" className="form-label">
                  Bidder_Name:
                </label>
                <input
                  type="text"
                  className="form-control"
                  id="bidder"
                  value={bidder}
                  onChange={handleBidderChange}
                />
              </div>
              <button type="submit" className="btn btn-submit mt-3 mb-4" onClick={handleSubmit}>
                Add
              </button>

              </form>
              </div>
              </div>
      )}
      </>
  )
      }

      export default Estimator;