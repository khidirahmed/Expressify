
import React from "react";
import styled from "styled-components";

const ProgressBar = ({ percentage, label }) => {
    return (
        <Container>
            <p>{label}</p>
            <Bar>
                <Fill style={{ width: `${percentage}%` }} />
            </Bar>
            <Percentage>{percentage}%</Percentage>
        </Container>
    );
};

export default ProgressBar;


const Container = styled.div`
  text-align: center;
  margin-top: 20px;
`;

const Bar = styled.div`
  width: 300px;
  height: 20px;
  background: #ffffff;
  border-radius: 10px;
  overflow: hidden;
  margin: 10px auto;
  border: 2px solid black;
`;

const Fill = styled.div`
    height: 100%;
    background: #9dff8d;
    transition: width 0.5s ease-in-out;
`;

const Percentage = styled.p`
  font-size: 18px;
  margin: 5px 0;
`;