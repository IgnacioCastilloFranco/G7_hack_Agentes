import React, { useState } from 'react';
import { 
  Box, 
  Card, 
  CardContent, 
  Typography, 
  TextField, 
  Button, 
  Paper,
  Chip,
  Avatar,
  Collapse,
  IconButton,
  Divider,
  Alert
} from '@mui/material';
import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import LightbulbIcon from '@mui/icons-material/Lightbulb';
import ReplayIcon from '@mui/icons-material/Replay';

import LoadingSpinner from '../UI/LoadingSpinner';
import ErrorMessage from '../UI/ErrorMessage';
import { verifyAnswer } from '../../services/gameService';

const Riddle = ({ game, onNewGame }) => {
  const [answer, setAnswer] = useState('');
  const [showHint, setShowHint] = useState(false);
  const [hintIndex, setHintIndex] = useState(0);
  const [result, setResult] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  
  const handleShowHint = () => {
    if (hintIndex < game.hints.length - 1) {
      setHintIndex(prev => prev + 1);
    }
    setShowHint(true);
  };
  
  const handleAnswerSubmit = async (e) => {
    e.preventDefault();
    if (!answer.trim()) return;
    
    setIsSubmitting(true);
    setError(null);
    
    try {
      const response = await verifyAnswer(game.id, answer);
      setResult(response);
    } catch (err) {
      setError(err);
    } finally {
      setIsSubmitting(false);
    }
  };
  
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
                {game.title}
              </Typography>
              <Chip 
                label={`Dificultad: ${game.difficulty === 'easy' ? 'Fácil' : game.difficulty === 'medium' ? 'Media' : 'Difícil'}`}
                color={game.difficulty === 'easy' ? 'success' : game.difficulty === 'medium' ? 'primary' : 'secondary'}
                size="small"
              />
            </Box>
            
            <Typography variant="body2" color="text.secondary" gutterBottom>
              {game.instructions}
            </Typography>
            
            <Paper 
              elevation={3} 
              sx={{ 
                p: 3, 
                my: 3, 
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
                  ¡Por mis bigotitos! Aquí tienes un acertijo mágico:
                </Typography>
              </Box>
              
              <Box sx={{ ml: 7 }}>
                <ReactMarkdown>
                  {game.content}
                </ReactMarkdown>
              </Box>
            </Paper>
            
            <Collapse in={showHint}>
              <Paper sx={{ p: 2, mb: 3, bgcolor: 'magic.light', borderRadius: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <LightbulbIcon color="warning" sx={{ mr: 1 }} />
                  <Typography variant="body2" sx={{ fontStyle: 'italic' }}>
                    {game.hints[hintIndex]}
                  </Typography>
                </Box>
              </Paper>
            </Collapse>
            
            {!result ? (
              <Box component="form" onSubmit={handleAnswerSubmit} sx={{ mt: 3 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <TextField
                    fullWidth
                    label="Tu respuesta"
                    variant="outlined"
                    value={answer}
                    onChange={(e) => setAnswer(e.target.value)}
                    disabled={isSubmitting}
                    sx={{ mr: 2 }}
                  />
                  <Button
                    variant="contained"
                    color="secondary"
                    onClick={handleShowHint}
                    disabled={hintIndex >= game.hints.length - 1 && showHint}
                    sx={{ minWidth: 100 }}
                  >
                    Pista
                  </Button>
                </Box>
                <Button
                  type="submit"
                  variant="contained"
                  fullWidth
                  disabled={!answer.trim() || isSubmitting}
                >
                  Comprobar
                </Button>
              </Box>
            ) : (
              <Box sx={{ mt: 3 }}>
                <Alert 
                  severity={result.correct ? "success" : "info"}
                  sx={{ mb: 2 }}
                >
                  <Typography variant="body1">
                    {result.feedback}
                  </Typography>
                  {result.reward && (
                    <Typography variant="body2" sx={{ mt: 1, fontWeight: 'bold' }}>
                      {result.reward}
                    </Typography>
                  )}
                </Alert>
                <Button
                  variant="outlined"
                  startIcon={<ReplayIcon />}
                  onClick={onNewGame}
                  fullWidth
                >
                  Nuevo juego
                </Button>
              </Box>
            )}
            
            {isSubmitting && <LoadingSpinner message="Consultando al Ratoncito..." />}
            {error && <ErrorMessage error={error} />}
          </CardContent>
        </Card>
      </motion.div>
    </Box>
  );
};

export default Riddle;