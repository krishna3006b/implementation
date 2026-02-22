import { motion } from 'framer-motion'
import { useLocation } from 'react-router-dom'

const pageVariants = {
    initial: { opacity: 0, y: 15, filter: 'blur(4px)' },
    in: { opacity: 1, y: 0, filter: 'blur(0px)' },
    out: { opacity: 0, scale: 0.98, filter: 'blur(4px)' }
};

const pageTransition = {
    type: 'tween',
    ease: 'circOut',
    duration: 0.4
};

export default function PageWrapper({ children }) {
    const location = useLocation()
    return (
        <motion.div
            key={location.pathname}
            initial="initial"
            animate="in"
            exit="out"
            variants={pageVariants}
            transition={pageTransition}
            style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column' }}
        >
            {children}
        </motion.div>
    )
}
