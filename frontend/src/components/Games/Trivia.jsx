import React, { useState } from 'react';
import { 
  Box, 
  Card, 
  CardContent, 
  Typography, 
  Button, 
  Paper,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormControl,
  LinearProgress,
  Avatar,
  Alert,
  Chip
} from '@mui/material';
import { motion } from 'framer-motion';

const Trivia = ({ questions, location, onNewGame }) => {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedOption, setSelectedOption] = useState('');
  const [score, setScore] = useState(0);
  const [answered, setAnswered] = useState(false);
  const [gameComplete, setGameComplete] = useState(false);
  
  const handleOptionSelect = (e) => {
    setSelectedOption(e.target.value);
  };
  
  const handleSubmit = () => {
    const isCorrect = selectedOption === questions[currentQuestion].correct;
    if (isCorrect) {
      setScore(score + 1);
    }
    setAnswered(true);
  };
  
  const handleNextQuestion = () => {
    setSelectedOption('');
    setAnswered(false);
    
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      setGameComplete(true);
    }
  };
  
  const progress = ((currentQuestion + 1) / questions.length) * 100;
  
  return (
    <Box sx={{ mb: 4 }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
      >
        <Card className="magic-card" variant="outlined">
          <CardContent>
            <Box sx={{ mb: 2, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Typography variant="h5" component="h2" sx={{ color: 'primary.main' }}>
                Trivia Mágica: {location}
              </Typography>
              <Chip 
                label={`Pregunta ${currentQuestion + 1} de ${questions.length}`}
                color="primary"
                size="small"
              />
            </Box>
            
            <LinearProgress 
              variant="determinate" 
              value={progress} 
              sx={{ mb: 3, height: 10, borderRadius: 5 }} 
            />
            
            {!gameComplete ? (
              <>
                <Paper 
                  elevation={3} 
                  sx={{ 
                    p: 3, 
                    mb: 3, 
                    borderRadius: 2,
                    position: 'relative',
                    overflow: 'hidden',
                    '&::before': {
                      content: '""',
                      position: 'absolute',
                      top: 0,
                      left: 0,
                      width: '100%',
                      height: '5px',
                      background: 'linear-gradient(90deg, #3f51b5, #f50057)'
                    }
                  }}
                >
                  <Box sx={{ display: 'flex', mb: 2 }}>
                    <Avatar 
                      src="/images/ratoncito.png" 
                      alt="Ratoncito" 
                      sx={{ mr: 2, bgcolor: 'primary.main' }}
                    >
                      🐭
                    </Avatar>
                    <Typography variant="body1">
                      {questions[currentQuestion].question}
                    </Typography>
                  </Box>
                  
                  <FormControl component="fieldset" sx={{ ml: 7, width: '100%' }}>
                    <RadioGroup value={selectedOption} onChange={handleOptionSelect}>
                      {questions[currentQuestion].options.map((option, index) => (
                        <FormControlLabel
                          key={index}
                          value={option}
                          disabled={answered}
                          control={
                            <Radio 
                              sx={{ 
                                color: answered && option === questions[currentQuestion].correct 
                                  ? 'success.main' 
                                  : undefined
                              }}
                            />
                          }
                          label={option}
                          sx={{ 
                            mb: 1, 
                            p: 1,
                            borderRadius: 1,
                            bgcolor: answered 
                              ? option === questions[currentQuestion].correct 
                                ? 'success.light'
                                : option === selectedOption ? 'error.light' : 'transparent'
                              : 'transparent',
                          }}
                        />
                      ))}
                    </RadioGroup>
                  </FormControl>
                </Paper>
                
                {answered ? (
                  <Box>
                    <Alert 
                      severity={selectedOption === questions[currentQuestion].correct ? "success" : "error"}
                      sx={{ mb: 2 }}
                    >
                      {selectedOption === questions[currentQuestion].correct 
                        ? "¡Por mis bigotitos! ¡Has acertado!" 
                        : `¡No pasa nada! La respuesta correcta era: ${questions[currentQuestion].correct}`
                      }
                    </Alert>
                    <Button
                      variant="contained"
                      color="primary"
                      fullWidth
                      onClick={handleNextQuestion}
                    >
                      {currentQuestion < questions.length - 1 ? "Siguiente Pregunta" : "Ver Resultados"}
                    </Button>
                  </Box>
                ) : (
                  <Button
                    variant="contained"
                    color="secondary"
                    fullWidth
                    disabled={!selectedOption}
                    onClick={handleSubmit}
                  >
                    Comprobar
                  </Button>
                )}
              </>
            ) : (
              <Box sx={{ textAlign: 'center', py: 3 }}>
                <Typography variant="h5" gutterBottom>
                  ¡Has completado la Trivia Mágica!
                </Typography>
                <Typography variant="h4" sx={{ color: 'primary.main', my: 2 }}>
                  Tu puntuación: {score} de {questions.length}
                </Typography>
                <Typography variant="body1" paragraph>
                  {score === questions.length 
                    ? "¡Por mis bigotes! ¡Eres un experto en Madrid!" 
                    : score >= questions.length / 2
                      ? "¡Muy bien! Conoces bastantes secretos de la ciudad"
                      : "Sigue explorando Madrid para conocer más secretos"
                  }
                </Typography>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={onNewGame}
                >
                  Jugar de nuevo
                </Button>
              </Box>
            )}
          </CardContent>
        </Card>
      </motion.div>
    </Box>
  );
};

export default Trivia;