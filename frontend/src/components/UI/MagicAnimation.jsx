import React, { useEffect, useState } from 'react';
import { Box } from '@mui/material';
import { motion } from 'framer-motion';

const MagicAnimation = ({ children }) => {
  const [bubbles, setBubbles] = useState([]);
  
  useEffect(() => {
    const newBubbles = Array.from({ length: 10 }, (_, i) => ({
      id: i,
      size: Math.random() * 40 + 10, 
      left: `${Math.random() * 100}%`,
      top: `${Math.random() * 100}%`,
      duration: Math.random() * 15 + 10, 
      delay: Math.random() * 5,
    }));
    
    setBubbles(newBubbles);
  }, []);
  
  return (
    <Box sx={{ position: 'relative', overflow: 'hidden' }}>
      {bubbles.map((bubble) => (
        <Box
          key={bubble.id}
          component={motion.div}
          className="magic-bubble"
          sx={{
            width: bubble.size,
            height: bubble.size,
            left: bubble.left,
            top: bubble.top,
          }}
          animate={{
            y: [0, -100, 0],
            opacity: [0.2, 0.7, 0.2],
          }}
          transition={{
            duration: bubble.duration,
            ease: "easeInOut",
            repeat: Infinity,
            delay: bubble.delay,
          }}
        />
      ))}
      
      <Box
        component={motion.div}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        sx={{ position: 'relative', zIndex: 1 }}
      >
        {children}
      </Box>
    </Box>
  );
};

export default MagicAnimation;