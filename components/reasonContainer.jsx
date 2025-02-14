
import React from "react";
import styled from "styled-components";

const ThoughtContainer = ({ text }) => {
    return (
        <Container>
            <Title>AI Reasoning</Title>
            <Box>{text}</Box>
        </Container>
    );
};

export default ThoughtContainer;

const Container = styled.div`
  text-align: center;
  margin-top: 30px;
`;

const Title = styled.h2`
  font-size: 24px;
  color: #333;
  margin-bottom: 10px;
`;

const Box = styled.div`
  width: 500px;
  min-height: 150px;
  background: #f4f4f4;
  border: 3px solid #333;
  border-radius: 10px;
  padding: 15px;
  font-size: 18px;
  color: #222;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
`;