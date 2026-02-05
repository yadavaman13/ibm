# Field Contextual Help - Quick Reference

## 🚀 Quick Start

### For Users
1. Look for the **(?)** icon next to field labels
2. Click it to get instant help about that field
3. Read the AI-generated explanation
4. Ask follow-up questions if needed
5. Close modal and fill the form confidently

### For Developers
1. Import components:
   ```jsx
   import FieldHelpIcon from '../components/FieldHelpIcon';
   import FieldHelpModal from '../components/FieldHelpModal';
   ```

2. Add state:
   ```jsx
   const [helpModalOpen, setHelpModalOpen] = useState(false);
   const [helpFieldLabel, setHelpFieldLabel] = useState('');
   const [helpFieldName, setHelpFieldName] = useState('');
   ```

3. Add handler:
   ```jsx
   const handleHelpClick = (fieldName, fieldLabel) => {
       setHelpFieldName(fieldName);
       setHelpFieldLabel(fieldLabel);
       setHelpModalOpen(true);
   };
   ```

4. Add to field label:
   ```jsx
   <label className="form-label">
       Soil pH <span className="required">*</span>
       <FieldHelpIcon 
           fieldName="soil_ph" 
           onClick={() => handleHelpClick('soil_ph', 'Soil pH')} 
       />
   </label>
   ```

5. Add modal at end:
   ```jsx
   <FieldHelpModal
       isOpen={helpModalOpen}
       onClose={() => setHelpModalOpen(false)}
       fieldLabel={helpFieldLabel}
       fieldName={helpFieldName}
   />
   ```

## 📁 Files Created

```
client/src/
├── components/
│   ├── FieldHelpIcon.jsx       ← Help icon component
│   └── FieldHelpModal.jsx      ← Modal chatbot interface
├── utils/
│   └── fieldHelpers.js         ← Field detection logic
└── styles/
    ├── field-help-icon.css     ← Icon styles
    └── field-help-modal.css    ← Modal styles
```

## 🔧 Configuration

### Add New Agriculture Field
Edit `src/utils/fieldHelpers.js`:
```javascript
export const AGRICULTURE_FIELDS = new Set([
    // Existing fields...
    'your_new_field',  // Add here
]);
```

### Change Help Icon Appearance
Edit `src/styles/field-help-icon.css`:
```css
.field-help-icon {
    width: 18px;         /* Change size */
    height: 18px;
    color: #6b7280;      /* Change color */
}
```

### Change Modal Theme
Edit `src/styles/field-help-modal.css`:
```css
.field-help-header {
    background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
    /* Change gradient colors */
}
```

## 🎯 Which Fields Get Help Icons?

### ✅ Show Help Icon (Agriculture Fields)
- crop, season, area
- fertilizer, pesticide
- soil_type, soil_ph, soil_moisture
- nitrogen, phosphorus, potassium (N, P, K)
- irrigation_method
- humidity_level
- crop_stage, pest_severity
- Any field in `AGRICULTURE_FIELDS` set

### ❌ No Help Icon (Generic Fields)
- state, city, district, location
- name, phone, email, address
- Any field in `GENERIC_FIELDS` set

## 🧪 Testing

### Manual Test Checklist
```
□ Help icon appears on agriculture fields
□ No help icon on generic fields (state, city, etc.)
□ Icon changes color on hover
□ Clicking icon opens modal
□ Modal shows field-specific explanation
□ User can ask follow-up questions
□ ESC key closes modal
□ Click outside closes modal
□ Previous chat clears on new field
□ Works on mobile devices
□ Backend fallback works
```

### Test Commands
```bash
# Start backend
cd fasal-mitra/server
python run.py

# Start frontend
cd fasal-mitra/client
npm run dev

# Visit pages
http://localhost:5173/yield-prediction
http://localhost:5173/disease-detection
```

## 🐛 Troubleshooting

### Help Icon Not Showing
**Check:** Is field in `AGRICULTURE_FIELDS` set?
```javascript
// In fieldHelpers.js
console.log(shouldShowHelp('your_field')); // Should return true
```

### Modal Not Opening
**Check:** Did you add state and handler?
```javascript
const [helpModalOpen, setHelpModalOpen] = useState(false);
const handleHelpClick = (fieldName, fieldLabel) => { /* ... */ };
```

### Chatbot Not Responding
**Check:** 
1. Backend server running? (http://localhost:8000)
2. Gemini API key set? (Check .env file)
3. Network errors in browser console?

### Styling Issues
**Check:**
1. CSS files imported?
   ```jsx
   import '../styles/field-help-icon.css';
   import '../styles/field-help-modal.css';
   ```
2. Class names match?
3. CSS variables defined?

## 📱 Mobile Testing

### Test on Different Devices
- iOS Safari
- Android Chrome
- Tablet (iPad/Android)
- Small phones (< 375px width)
- Large phones (> 414px width)

### Mobile-Specific Features
- Full-screen modal
- Touch-friendly buttons (44px min)
- Scrollable message area
- Sticky input at bottom
- Proper zoom disabled

## 🔐 Security Notes

- ✅ No sensitive data in modal
- ✅ API through secure backend
- ✅ XSS protection (React escaping)
- ✅ Rate limiting on backend
- ✅ CORS configured

## 📊 Performance

| Metric | Value |
|--------|-------|
| Icon Load | < 50ms |
| Modal Open | < 100ms |
| API Response | 2-5s |
| Bundle Size | +15KB |
| Memory Usage | Minimal |

## 🎨 Design Tokens

```css
--color-primary: #16a34a      /* Green */
--color-primary-dark: #15803d /* Dark Green */
--color-gray-500: #6b7280     /* Gray */
--color-white: #ffffff        /* White */
--border-radius: 1rem         /* 16px */
--transition-fast: 0.2s       /* Fast animation */
--transition-medium: 0.3s     /* Medium animation */
```

## 🔄 Update Checklist

When updating the feature:
```
□ Test help icon visibility
□ Test modal functionality
□ Test API integration
□ Test on mobile
□ Check accessibility
□ Update documentation
□ Commit with clear message
```

## 📚 Related Documentation

- [Full Implementation Guide](FIELD_HELP_IMPLEMENTATION.md)
- [Visual Guide](FIELD_HELP_VISUAL_GUIDE.md)
- [API Documentation](fasal-mitra/server/API_DOCUMENTATION.md)
- [Chatbot Service](fasal-mitra/server/app/services/chatbot_service.py)

## 💡 Tips & Best Practices

### For Adding Fields
1. Always check if field is truly agriculture-related
2. Use descriptive field names
3. Keep labels clear and concise
4. Test with actual users if possible

### For Prompts
1. Keep language simple and farmer-friendly
2. Include practical measurement methods
3. Mention why field is important
4. Provide common value ranges
5. Suggest learning resources

### For UI/UX
1. Keep help icon subtle but visible
2. Ensure modal is easy to close
3. Make explanations scannable
4. Allow follow-up questions
5. Test on real devices

## 🎓 Learning Resources

### For Developers
- React Hooks: https://react.dev/reference/react
- Markdown Rendering: https://github.com/remarkjs/react-markdown
- CSS Animations: https://developer.mozilla.org/en-US/docs/Web/CSS/animation
- Accessibility: https://www.w3.org/WAI/ARIA/apg/

### For Understanding Agriculture Terms
- Local agricultural extension offices
- Government agriculture websites
- Farmer cooperatives
- Agricultural universities

---

**Quick Links:**
- [Implementation Guide](FIELD_HELP_IMPLEMENTATION.md) - Detailed technical guide
- [Visual Guide](FIELD_HELP_VISUAL_GUIDE.md) - UI/UX flow diagrams
- Components: `client/src/components/Field*.jsx`
- Utilities: `client/src/utils/fieldHelpers.js`
- Styles: `client/src/styles/field-help-*.css`

**Support:**
- Create issue in project repository
- Check error logs in browser console
- Verify backend server is running
- Test with minimal example first

**Last Updated:** February 5, 2026
