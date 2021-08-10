const SOSBtn = document.querySelector('.sos_btn');
const pageLoader = document.querySelector('.page-loader');

SOSBtn.addEventListener('click', () => {
  pageLoader.classList.toggle('loading');
  navigator.geolocation.getCurrentPosition(
    async function (pos) {
      let crd = pos.coords;
      const res = await fetch(
        `/send-message?latitude=${crd.latitude}&longitude=${crd.longitude}`,
        { method: 'POST' }
      );
      if (res.status === 201) {
        alert('SOS alert sent successfully');
      } else {
        alert('Could not sent SOS alert');
      }
      pageLoader.classList.toggle('loading');
    },
    (err) => {
      alert('Could not sent SOS alert');
      console.error(err);
    }
  );
});
