const SOSBtn = document.querySelector('.sos_btn');

SOSBtn.addEventListener('click', () => {
  navigator.geolocation.getCurrentPosition(
    async function (pos) {
      let crd = pos.coords;
      const res = await fetch(
        `/send-message?latitude=${crd.latitude}&longitude=${crd.longitude}`,
        { method: 'POST' }
      );
      if (res.status === 200) {
        alert('SOS alert sent successfully');
      }
    },
    (err) => {
      alert('Could not sent SOS alert');
      console.error(err);
    }
  );
});
