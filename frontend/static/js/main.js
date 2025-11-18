// Daily questions loader
document.addEventListener("DOMContentLoaded", function () {
  const dailyBtn = document.getElementById("load-daily-btn");
  const dailyContainer = document.getElementById("daily-container");

  if (dailyBtn && dailyContainer) {
    dailyBtn.addEventListener("click", async () => {
      dailyContainer.innerHTML = "Loading...";
      try {
        const res = await fetch("/app/daily");
        if (!res.ok) throw new Error("Failed to load");
        const data = await res.json();

        if (!data.questions || data.questions.length === 0) {
          dailyContainer.innerHTML = "No questions found for today.";
          return;
        }

        dailyContainer.innerHTML = `
          <p><strong>Level ${data.level}</strong> · ${data.date}</p>
        `;

        data.questions.forEach((q, idx) => {
          const div = document.createElement("div");
          div.className = "rr-daily-question";
          div.innerHTML = `
            <p>${idx + 1}. ${q.text}</p>
            <ul class="rr-small">
              <li>A. ${q.options.A}</li>
              <li>B. ${q.options.B}</li>
              <li>C. ${q.options.C}</li>
              <li>D. ${q.options.D}</li>
            </ul>
            <p class="rr-small">Try answering in your head or with a friend, then play the level quiz!</p>
          `;
          dailyContainer.appendChild(div);
        });
      } catch (err) {
        dailyContainer.innerHTML = "Error loading daily questions.";
      }
    });
  }

  // Avatar change on profile page
  const avatarChooser = document.getElementById("avatar-chooser");
  const avatarStatus = document.getElementById("avatar-status");

  if (avatarChooser) {
    avatarChooser.addEventListener("click", async (e) => {
      const btn = e.target.closest("button[data-avatar]");
      if (!btn) return;
      const avatar = btn.getAttribute("data-avatar");

      try {
        const res = await fetch("/app/avatar", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ avatar }),
        });
        const data = await res.json();
        if (data.status === "ok") {
          if (avatarStatus) avatarStatus.textContent = "Avatar updated!";
          // simple reload to apply avatar in header/dashboard
          setTimeout(() => window.location.reload(), 400);
        } else {
          if (avatarStatus) avatarStatus.textContent = "Could not update avatar.";
        }
      } catch (err) {
        if (avatarStatus) avatarStatus.textContent = "Error talking to server.";
      }
    });
  }
});
