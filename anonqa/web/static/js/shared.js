const is_mobile = function () {
  let check = false;
  (function (a) {
    if (
      /(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino|android|ipad|playbook|silk/i.test(
        a,
      ) ||
      /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(
        a.substr(0, 4),
      )
    )
      check = true;
  })(navigator.userAgent || navigator.vendor || window.opera);
  return check;
};

document.body.classList.add(is_mobile() ? "ua-mobile" : "ua-desktop");

let tg = window.Telegram.WebApp;

document.body.classList.add(
  tg.colorScheme == "dark" ? "tg-scheme--dark" : "tg-scheme--light",
);

const exec_with_retry = (callback) => {
  try {
    callback();
  } catch (e) {
    setTimeout(() => {
      exec_with_retry(callback);
    }, 50);
  }
};

const fadein = (elem, display) => {
  elem.style.animation = "";
  elem.style.display = display || "block";
  elem.classList.remove("fadeout");
  elem.classList.add("fadein");
};

const fadeout = (elem) => {
  elem.style.animation = "";
  elem.classList.remove("fadein");
  elem.classList.add("fadeout");
  setTimeout(() => {
    elem.style.display = "none";
  }, 250);
};

window.closeModal = () => {
  fadeout(document.querySelector(".modal-darkener"));
  fadeout(document.querySelector(".modal"));
  document.querySelector(".modal-close").removeEventListener("click", () => { });
  document
    .querySelector(".modal-darkener")
    .removeEventListener("click", () => { });
};

window.showModal = (title, content, tgs, closable = true) => {
  tg.expand();
  if (document.querySelector(".modal").classList.contains("modal-prompt")) {
    document.querySelector(".modal").classList.remove("modal-prompt");
  }
  document.querySelector(".modal-title").innerHTML = title;
  document.querySelector(".modal-content").innerHTML = content;
  if (tgs) {
    document.querySelector("#modal-tgs-player").style.display = "block";
    exec_with_retry(() => {
      document.querySelector("#modal-tgs-player").load(tgs);
    });
    fadein(document.querySelector(".modal-darkener"));
    fadein(document.querySelector(".modal"));
    if (!closable) return;
    document.querySelector(".modal-close").addEventListener("click", () => {
      window.closeModal();
      tg.HapticFeedback.selectionChanged();
    });
    document.querySelector(".modal-darkener").addEventListener("click", () => {
      window.closeModal();
    });
  } else {
    document.querySelector("#modal-tgs-player").style.display = "none";
    fadein(document.querySelector(".modal-darkener"));
    fadein(document.querySelector(".modal"));
    if (!closable) return;
    document.querySelector(".modal-close").addEventListener("click", () => {
      window.closeModal();
      tg.HapticFeedback.selectionChanged();
    });
    document.querySelector(".modal-darkener").addEventListener("click", () => {
      window.closeModal();
    });
  }
};

window.showPrompt = (
  title,
  content,
  placeholder,
  button_text,
  input_type,
  callback,
  tgs,
) => {
  tg.expand();
  document.querySelector(".modal").classList.add("modal-prompt");
  document.querySelector(".modal-title").innerHTML = title;
  document.querySelector(".modal-content").innerHTML = content;
  document.querySelector(".modal-input").placeholder = placeholder;
  document.querySelector(".modal-input").type = input_type;
  document.querySelector(".modal-input").value = "";
  document.querySelector(".modal-button").value = button_text;
  if (tgs) {
    document.querySelector("#modal-tgs-player").style.display = "block";
    exec_with_retry(() => {
      document.querySelector("#modal-tgs-player").load(tgs);
    });
    fadein(document.querySelector(".modal-darkener"));
    fadein(document.querySelector(".modal"));
    document.querySelector(".modal-close").addEventListener("click", () => {
      window.closeModal();
      tg.HapticFeedback.selectionChanged();
    });
    document.querySelector(".modal-darkener").addEventListener("click", () => {
      window.closeModal();
    });
  } else {
    document.querySelector("#modal-tgs-player").style.display = "none";
    fadein(document.querySelector(".modal-darkener"));
    fadein(document.querySelector(".modal"));
    document.querySelector(".modal-close").addEventListener("click", () => {
      window.closeModal();
      tg.HapticFeedback.selectionChanged();
    });
    document.querySelector(".modal-darkener").addEventListener("click", () => {
      window.closeModal();
    });
  }
  document.querySelector(".modal-button").addEventListener("click", () => {
    callback(document.querySelector(".modal-input").value);
    window.closeModal();
  });
};

window.smoothScrollTo = (element, padding = 5) => {
  const y = element.getBoundingClientRect().top + window.scrollY - padding;
  window.scroll({
    top: y,
    behavior: "smooth",
  });
};

const activate_blur = () => {
  tg.HapticFeedback.selectionChanged();
  document.body.classList.add("blur");
  document.querySelector(".choose").style.animation =
    ".3s ease movingfadein forwards";
  setTimeout(() => {
    window.smoothScrollTo(document.querySelector(".choose"));
  }, 50);
  tg.expand();
};

const deactivate_blur = () => {
  document.body.classList.remove("blur");
  let elem = document.querySelector(".choose");
  elem.classList.remove("choose");
  elem.style.animation = ".3s ease movingfadeout forwards";
  window.smoothScrollTo(elem, 15);
};

const get_form_json = (elem) => {
  var data = new FormData(elem ? elem : document.querySelector("form"));
  var json = {};
  data.forEach(function (value, key) {
    json[key] = value;
  });
  return json;
};

document.querySelectorAll(".showhide").forEach((elem) => {
  elem.addEventListener("click", () => {
    let target = document.querySelector(elem.dataset.target);
    if (target.getAttribute("type") == "password") {
      target.setAttribute("type", "text");
    } else {
      target.setAttribute("type", "password");
    }
    elem.classList.toggle("active");
  });
});

const monospace_callback = (e) => {
  let text = e.target.innerText;
  navigator.clipboard.writeText(text).then(() => {
    tg.HapticFeedback.selectionChanged();
  });
};

const process_spoiler = (elem) => {
  let hide = elem.querySelector(".hide");
  function dots() {
    let dot = document.createElement("div");
    dot.className = "dot";
    dot.style.top = `${hide.offsetHeight * Math.random()}px`;
    dot.style.left = `${hide.offsetWidth * Math.random()}px`;
    let size = Math.random() * 2;
    dot.style.height = `${size}px`;
    dot.style.width = `${size}px`;
    dot.style.animationDelay = `${Math.random() * 3}s`;
    dot.style.setProperty("--seedx", `${Math.random() + 0.7}`);
    dot.style.setProperty("--seedy", `${Math.random() + 0.7}`);
    hide.appendChild(dot);
  }
  for (let i = 0; i < 25 * elem.querySelector(".text").innerText.length; i++) {
    dots();
  }
};

const unhide_spoiler = (elem, text) => {
  elem.querySelector(".text").innerText = text;
  elem.classList.add("open");
  fadeout(elem.querySelector(".hide"));
};

const api = (
  method,
  url,
  headers,
  data,
  error_title,
  error_body,
  recaptcha,
  manual_api_error_handling,
) => {
  var request_id = Math.random().toString(16).substring(2);
  var recaptcha = recaptcha ? `?g_recaptcha_response=${recaptcha}` : "";
  return new Promise((resolve, reject) => {
    axios({
      method: method,
      url: `/api${url}${recaptcha}`,
      headers: {
        "Content-Type": "application/json",
        "X-Request-ID": request_id,
        ...(headers ? headers : {}),
        ...window.authHeaders,
      },
      data: data,
    })
      .then((response) => {
        if (response.data.success === false) {
          if (manual_api_error_handling) {
            resolve(response.data);
            return;
          }
          throw new Error("API error");
        }
        resolve(response.data);
      })
      .catch((error) => {
        if (error.response && error.response.status == 401 && error_title) {
          tg.CloudStorage.getKeys((err, keys) => {
            if (!err && keys) {
              tg.CloudStorage.removeItems(keys, () => {
                window.location.href = "/login";
              });
            } else {
              window.location.href = "/login";
            }
          });
          return;
        }

        if (error_title) {
          window.showModal(
            error_title,
            error_body
              ? error_body
              : `Please, contact the developer. Tell him this code: <span class="monospace">${request_id}</span>`,
            "/static/img/tgs/sad.tgs",
          );
          if (!error_body) {
            document
              .querySelector(".modal .monospace")
              .addEventListener("click", monospace_callback);
          }
        }
        tg.HapticFeedback.notificationOccurred("error");
        console.error("Error:", error);
        reject(error);
      });
  });
};

async function sha256(message) {
  const msgBuffer = new TextEncoder().encode(message);
  const hashBuffer = await crypto.subtle.digest("SHA-256", msgBuffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
  return hashHex;
}

window.addEventListener("load", () => {
  var url = new URL(window.location.href);
  window.recipientTag = url.searchParams.get("r");
  if (!window.recipientTag) {
    window.showModal(
      "Error",
      "No recipient specified.",
      "/static/img/tgs/cross.tgs",
      false,
    );
    return;
  }

  document.querySelector("form").addEventListener("submit", (e) => {
    e.preventDefault();

    if (!get_form_json().message) {
      window.showModal(
        "Error",
        "Message cannot be empty.",
        "/static/img/tgs/cross.tgs",
      );
      return;
    }

    document.querySelector("input[type=submit]").classList.add("submitted");
    document.querySelector("input[type=submit]").disabled = true;
    tg.HapticFeedback.selectionChanged();

    grecaptcha.ready(function () {
      grecaptcha
        .execute("6LcJrDkpAAAAAJ5PanLaBwmsEFcwwIzcGYS8OejR", {
          action: "submit",
        })
        .then((token) => {
          api(
            "POST",
            "/v1/send",
            {},
            JSON.stringify({
              recipient_tag: window.recipientTag,
              sender: tg.initData,
              message: get_form_json().message,
            }),
            "Failed to send message",
            null,
            token,
          )
            .then((response) => {
              if (response.status === "success") {
                document.querySelector("form").reset();
                window.showModal(
                  "Success",
                  response.message,
                  "/static/img/tgs/tada.tgs",
                );
                document.querySelector("textarea").value = "";
              } else {
                window.showModal(
                  "Error",
                  `Raccoons broke something again... ${response.message}`,
                  "/static/img/tgs/raccoon.tgs",
                );
              }
            })
            .catch((error) => { })
            .finally(() => {
              document
                .querySelector("input[type=submit]")
                .classList.remove("submitted");
              document.querySelector("input[type=submit]").disabled = false;
            });
        });
    });
  });
  document.querySelector("input[type=submit]").disabled = false;
});
